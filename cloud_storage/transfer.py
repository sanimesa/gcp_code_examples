#https://cloud.google.com/storage/docs/samples/storage-transfer-manager-upload-many

def upload_many_blobs_with_transfer_manager(
    bucket_name, filenames, source_directory="", workers=8
):
    """Upload every file in a list to a bucket, concurrently in a process pool.

    Each blob name is derived from the filename, not including the
    `source_directory` parameter. For complete control of the blob name for each
    file (and other aspects of individual blob metadata), use
    transfer_manager.upload_many() instead.
    """

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # A list (or other iterable) of filenames to upload.
    # filenames = ["file_1.txt", "file_2.txt"]

    # The directory on your computer that is the root of all of the files in the
    # list of filenames. This string is prepended (with os.path.join()) to each
    # filename to get the full path to the file. Relative paths and absolute
    # paths are both accepted. This string is not included in the name of the
    # uploaded blob; it is only used to find the source files. An empty string
    # means "the current working directory". Note that this parameter allows
    # directory traversal (e.g. "/", "../") and is not intended for unsanitized
    # end user input.
    # source_directory=""

    # The maximum number of processes to use for the operation. The performance
    # impact of this value depends on the use case, but smaller files usually
    # benefit from a higher number of processes. Each additional process occupies
    # some CPU and memory resources until finished. Threads can be used instead
    # of processes by passing `worker_type=transfer_manager.THREAD`.
    # workers=8

    from google.cloud.storage import Client, transfer_manager

    storage_client = Client()
    bucket = storage_client.bucket(bucket_name)

    results = transfer_manager.upload_many_from_filenames(
        bucket, filenames, source_directory=source_directory, max_workers=workers
    )

    for name, result in zip(filenames, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print("Failed to upload {} due to exception: {}".format(name, result))
        else:
            print("Uploaded {} to {}.".format(name, bucket.name))


bucket_name = "nimesa_bucket01"
filenames = ["Birthday theme - Made with Clipchamp.mp4", "OpenAI Article - Made with Clipchamp.mp4"]

if __name__ == '__main__':
    import time

    start_time = time.time()
    upload_many_blobs_with_transfer_manager(bucket_name, filenames, source_directory="C:/temp/", workers=8)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time with 8 workers: {elapsed_time} seconds")

    start_time = time.time()
    upload_many_blobs_with_transfer_manager(bucket_name, filenames, source_directory="C:/temp/", workers=2)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time with 2 workers: {elapsed_time} seconds")    