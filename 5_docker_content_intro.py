from stages import PrintStage, ConcurrentRunner, run_pipeline

from mock_docker import DockerStart, DownloadContent




def docker_content_intro():
    print("Docker has 4 content types, but lets ignore tags and talk about the 3 main"
          " units.")
    print("Blobs are large file, manifests and manifest lists are small files.")
    print("A manifest List references manifests.")
    print("A manifest references blobs.")
    print()
    print()
    print("I've written a mock docker library to demonstrate.")
    print("The model number is helpful for seeing how units relate to each other.")
    print("Manifest Lists are represented as integers.")
    print("Manifests are represented as tenths, <ML num>.1, <ML num>.2")
    print("Blobs are represented as 100ths, <ML num>.<M num>.1 <ML num>.<M num>.2")
    print()
    print()
    print("Each content has a single file, so we will talk about downloading content,"
          " but in Pulp terms, what we are really doing is downloading an Artifact.")
    print("For a Docker sync task, each file/content must be downloaded, processed, "
          " and saved.")
    print("To make this easy to see, the mock docker library will show the state of each "
          "content when printed.")
    print("`D` is downloaded, `P` is processed, `S` is saved.")
    print("(![d|p|s]) means that that this step has not yet happened for this content.")
    print("Blobs don't need to be processed so they always show P.")
    make_content = DockerStart(blobs=1, manifests=1, manifest_lists=1)
    print_them = PrintStage()
    stages = [make_content, print_them]
    run_pipeline(stages)


docker_content_intro()
