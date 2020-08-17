import pytest

from datacroaker import SingleVersionRemoteDataSource, RollingReleaseRemoteDataSource, \
    VersionAccessibleRemoteDataSource


def test_instances(tmp_path):
    SingleVersionRemoteDataSource(root_dir=tmp_path)
    RollingReleaseRemoteDataSource(root_dir=tmp_path)
    VersionAccessibleRemoteDataSource(root_dir=tmp_path)
