import os
import logging
import shutil

from datacroaker.datasourceinstance import DataSourceInstance

log = logging.getLogger(__name__)


class BaseDataSource():

    def __init__(self, root_dir):
        self.root_dir = root_dir

        self.name = self.__class__.__name__

        # set the data source directory (using class name)
        self._ds_dir = os.path.join(self.root_dir, self.__class__.__name__)
        if not os.path.exists(self.ds_dir):
            os.mkdir(self.ds_dir)

    @property
    def ds_dir(self):
        return self._ds_dir

    @ds_dir.setter
    def ds_dir(self, value):
        self._ds_dir = value

    def list_instances(self):
        return os.listdir(self.ds_dir)

    def current_downloads_in_process(self):
        """
        Return a list of current instances that are in process.
        """
        instances_in_process = []
        for instance in self.list_instances():
            if instance.startswith('process_'):
                instances_in_process.append(instance)
        return instances_in_process

    @property
    def instances_local(self):
        """
        Load all instances of this DataSource.
        """
        for instance in self.list_instances():
            if 'error_' not in instance and 'process_' not in instance and not instance.startswith('.'):
                yield self.get_instance_by_uuid(instance)

    def clear_datasource_directory(self):
        """
        Delete all local instances.
        """
        log.debug("Clear DataSource directory {}".format(self.ds_dir))
        for instance in self.list_instances():
            if not instance.startswith('.'):
                instance_path = os.path.join(self.ds_dir, instance)
                shutil.rmtree(instance_path)

    def get_instance_by_uuid(self, uuid):
        instance_path = os.path.join(self.ds_dir, uuid)

        if os.path.exists(instance_path):
            return DataSourceInstance.read(self, instance_path)

    def latest_local_instance(self):
        """
        Get local instance with latest 'instance_created' property.

        :return: The latest local instance.
        """
        latest = None
        for instance in self.instances_local:
            if not latest:
                latest = instance
            else:
                if instance.instance_created > latest.instance_created:
                    latest = instance
        return latest


class RemoteDataSource(BaseDataSource):

    def __init__(self, root_dir):
        super(RemoteDataSource, self).__init__(root_dir)

    def pre_download(self):
        """
        Settings and changes before a download becomes active.
        """
        pass

    def post_download(self):
        """
        Settings and changes after a download (independent of success/error).
        """
        pass


class RollingReleaseRemoteDataSource(RemoteDataSource):

    def __init__(self, root_dir):
        super(RollingReleaseRemoteDataSource, self).__init__(root_dir)


class VersionAccessibleRemoteDataSource(RemoteDataSource):

    def __init__(self, root_dir):
        super(VersionAccessibleRemoteDataSource, self).__init__(root_dir)

    def all_remote_versions(self):
        raise NotImplementedError

    def latest_remote_version(self):
        return max(self.all_remote_versions())

    def version_downloadable(self, version):
        """
        Check if version is downloadable.
        """
        if version in self.all_remote_versions():
            return True


class SingleVersionRemoteDataSource(VersionAccessibleRemoteDataSource):
    """
    DataSource class for a remote data source with defined versions where only
    one (usually the last one) version can be downloaded.
    """

    def __init__(self, root_dir):
        super(SingleVersionRemoteDataSource, self).__init__(root_dir)

    def version_downloadable(self, version):
        """
        Check if version is downloadable.
        """
        if version == self.latest_remote_version():
            return True
