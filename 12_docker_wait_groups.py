from stages import (PrintStage, PrintAndPassStage, ConcurrentRunner, run_pipeline, StageGroup,
                    WaitUntilComplete)

from mock_docker import DockerStart, DownloadContent, ProcessContent, SaveContent, ContentRelations


def docker_concurrent_wait_groups():
    print("So, how can we make our concurrency work better, reduce memory, "
          "and not mess up our many-to-many relationships?")
    print("Since StageGroups are treated as regular Stages, we can use the "
          "ConcurrentRunner with a whole group.")
    print("We also know that nested content is created from content higher up "
          "in the heirarchy. So, related content can be kept separate, running "
          " inside of a stage group, allowing the wait stage to only wait on the "
          " content that we know will be related.")
    print("We just need to shift our stages around a little.")
    make_content = DockerStart(blobs=1, manifests=1, manifest_lists=1)
    download_content = ConcurrentRunner(DownloadContent())
    process = ProcessContent()
    save_stage = SaveContent()
    handle_content = StageGroup([download_content, process, save_stage])
    wait_stage = WaitUntilComplete()
    relate_content = ContentRelations()
    content_stream = ConcurrentRunner(
        StageGroup([handle_content, handle_content, handle_content, wait_stage, relate_content])
    )
    print_end = PrintStage()
    stages = [make_content, content_stream, print_end]
    run_pipeline(stages)
    print("We still had to do some waiting, but items were able to pass through in chuncks, "
          "rather than all at once.")


docker_concurrent_wait_groups()
