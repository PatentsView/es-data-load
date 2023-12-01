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

    # CSV Load test
    test_mapping_folder = "tests/mappings/artifacts/csv_citation_load/"
    full_test_mapping_path = "{root}/{relative_folder_path}".format(
        relative_folder_path=test_mapping_folder, root=project_root
    )
    lj = LoadConfiguration.generate_load_configuration_from_folder(
        [full_test_mapping_path]
    )
    assert len(lj.get_load_operation_names()) == 1


def test_process_load_operation(
        pv_citations_only_schema_manager,
        load_job_configuration_1: LoadConfiguration,
        search,
        mysql_source,
):
    load_job = LoadJob(
        load_configuration=load_job_configuration_1,
        data_source=mysql_source,
        search_wrapper=search,
        test=False,
    )
    name_load_job_to_process = load_job_configuration_1.get_load_operation_names()[0]

    pv_citations_only_schema_manager.create_es_indices(
        drop_and_recreate=True, exists_ok=True
    )

    load_job.process_load_operation(name_load_job_to_process)
    assert_es_counts(
        search=load_job.search_wrapper,
        target_setting=load_job.load_configuration.get_load_operation(
            name_load_job_to_process
        )["target_setting"],
    )
    search.es.indices.delete(index=load_job.load_configuration.get_load_operation(
        name_load_job_to_process
    )["target_setting"]["index"])


def test_get_load_job_status(load_job: LoadJob):
    name_load_job_to_process = load_job.load_configuration.get_load_operation_names()[0]
    try:
        load_job.search_wrapper.es.indices.delete(
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
    for load_operation in load_job.load_configuration.get_load_operation_names():
        try:
            load_job.search_wrapper.es.indices.delete(
                index=load_job.load_configuration.get_load_operation(
                    load_operation
                )["target_setting"]["index"]
            )
        except NotFoundError:
            pass


def test_process_csv_load_operation(
        pv_citations_only_schema_manager,
        load_job_configuration_csv: LoadConfiguration,
        search,
        tabular_source,
):
    load_job = LoadJob(
        load_configuration=load_job_configuration_csv,
        data_source=tabular_source,
        search_wrapper=search,
        test=False,
    )
    name_load_job_to_process = load_job_configuration_csv.get_load_operation_names()[0]
    pv_citations_only_schema_manager.create_es_indices(
        exists_ok=True, drop_and_recreate=True
    )
    load_job.process_load_operation(name_load_job_to_process)
    target_setting = load_job.load_configuration.get_load_operation(
        name_load_job_to_process
    )["target_setting"]
    search.es.indices.refresh(index=target_setting["index"])
    count_response = search.es.count(index=target_setting["index"])
    print(count_response)
    assert count_response["count"] == 100
    hits = search.es.search(
        index=target_setting["index"],
        body={"query": {"term": {"patent_number": "9487532"}}},
    )
    assert not hits["timed_out"]
    assert hits["hits"]["total"]["value"] == 1
    hits = search.es.search(
        index=target_setting["index"],
        body={"query": {"term": {"cited_patent_number": "6218953"}}},
    )
    assert not hits["timed_out"]
    assert hits["hits"]["total"]["value"] == 1
    try:
        search.es.indices.delete(
            index=load_job.load_configuration.get_load_operation(
                name_load_job_to_process
            )["target_setting"]["index"]
        )
    except NotFoundError:
        pass
