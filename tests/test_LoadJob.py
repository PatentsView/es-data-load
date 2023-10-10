import os

import pytest
from elasticsearch import NotFoundError

from es_data_load.specification import LoadConfiguration, LoadJob
from tests.test_es import assert_es_counts


def test_generate_load_job_from_folder(project_root, config):
    test_mapping_folder = "tests/mappings/artifacts/patent_citations_loads"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
        relative_folder_path=test_mapping_folder, root=project_root
    )
    lj = LoadConfiguration.generate_load_configuration_from_folder(
        [full_test_mapping_path]
    )
    assert len(lj.get_load_operation_names()) == 1
    test_mapping_folder = "tests/mappings/artifacts/all_citations_loads"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
        relative_folder_path=test_mapping_folder, root=project_root
    )

    lj = LoadConfiguration.generate_load_configuration_from_folder(
        [full_test_mapping_path]
    )
    assert len(lj.get_load_operation_names()) == 2
    with pytest.raises(Exception):
        lj = LoadConfiguration.generate_load_configuration_from_folder(
            [os.path.join(full_test_mapping_path, "patent_citation.json")]
        )


def test_process_load_operation(
    load_job_configuration_1: LoadConfiguration,
    search,
    mysql_source,
):
    load_job = LoadJob(
        load_configuration=load_job_configuration_1,
        data_source=mysql_source,
        data_target=search,
        test=False,
    )
    name_load_job_to_process = load_job_configuration_1.get_load_operation_names()[0]
    try:
        load_job.search_target.es.indices.delete(
            index=load_job_configuration_1.get_load_operation(name_load_job_to_process)[
                "target_setting"
            ]["index"]
        )
    except NotFoundError:
        pass
    load_job.process_load_operation(name_load_job_to_process)
    assert_es_counts(
        search=load_job.search_target,
        target_setting=load_job.load_configuration.get_load_operation(
            name_load_job_to_process
        )["target_setting"],
    )


def test_get_load_job_status(load_job: LoadJob):
    name_load_job_to_process = load_job.load_configuration.get_load_operation_names()[0]
    try:
        load_job.search_target.es.indices.delete(
            index=load_job.load_configuration.get_load_operation(
                name_load_job_to_process
            )["target_setting"]["index"]
        )
    except NotFoundError:
        pass
    load_job.process_all_load_operations()
    status = load_job.get_load_results(name_load_job_to_process)
    assert all(
        x in status.keys()
        for x in ["batches", "record_count", "complete", "success", "duration"]
    )
    assert status["complete"] and ["success"]
