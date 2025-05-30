exports = async function () {
  // Number of days of data to retain — older data will be archived and deleted
  const DAYS_TO_SUBTRACT = 160;

  // Get current date and calculate the cutoff date
  const currentDate = new Date();
  const startDate = new Date(currentDate.getTime() - DAYS_TO_SUBTRACT * 24 * 60 * 60 * 1000);
  const currentEpochMs = currentDate.getTime(); // Used for generating a unique filename

  // Configuration constants for services, database, and collection
  const ARCHIVE_SERVICE = 's3FederatedArchive';  // S3-linked Atlas Data Federation service
  const CLUSTER_SERVICE = 'DemoCluster';         // Primary Atlas Cluster
  const DB_NAME = 'logs';                        // Database name
  const COLL_NAME = 'database';                  // Collection name
  const BUCKET_NAME = 'atlas-federated-archive'; // S3 bucket name for archive

  // Define source and archive collection handles
  const archiveColl = context.services.get(ARCHIVE_SERVICE).db(DB_NAME).collection(COLL_NAME);
  const sourceColl = context.services.get(CLUSTER_SERVICE).db(DB_NAME).collection(COLL_NAME);

  // Construct S3 filename path following the desired folder structure and timestamp
  const fileName = `databaseLogs/DemoCluster/${DB_NAME}/${COLL_NAME}/${currentEpochMs}/`;

  try {
    console.log(`Starting archive for documents before ${startDate.toISOString()}`);

    // Step 1: Archive documents older than the cutoff date to S3 as Parquet
    const archivePipeline = [
      {
        $match: {
          timestamp: { $lt: startDate } // Filter documents by timestamp
        }
      },
      {
        $out: {
          s3: {
            bucket: BUCKET_NAME,
            filename: fileName,
            format: {
              name: 'parquet',
              maxFileSize: '262144000B' // Set max file size to 250 MiB
            }
          }
        }
      }
    ];

    // Execute the archive pipeline
    await archiveColl.aggregate(archivePipeline).toArray();
    console.log(`Archive complete: ${fileName}`);

    // Step 2: Delete archived documents from the original collection
    const deleteResult = await sourceColl.deleteMany({ timestamp: { $lt: startDate } });
    console.log(`Deleted ${deleteResult.deletedCount} archived log records.`);
  } catch (err) {
    // Catch and log any errors encountered during archive or deletion
    console.error('Error during archive or delete operation:', err.message);
  }
};