exports = async function () {
  const DAYS_TO_SUBTRACT = 160; // Number of days to subtract from the current date

  const currentDate = new Date();
  const start_date = new Date(currentDate.getTime() - DAYS_TO_SUBTRACT * 24 * 60 * 60 * 1000); // Subtract days from the current date

  // Get the 'logs' collection from the 'prodArchive' database in the 'FederatedArchive' service
  const collName = context.services.get('FederatedArchive').db('prodArchive').collection('logs');

  // Define the aggregation pipeline for archiving
  const pipeline = [
    {
      $match: {
        timestamp: {
          $lt: start_date
        }
      }
    },
    {
      $out: {
        s3: {
          bucket: 'mongodb-user-demo-bucket',
          region: 'eu-central-1',
          filename: `${start_date.toISOString().replace(/:/g, '-')}Z-${currentDate.toISOString().replace(/:/g, '-')}Z`,
          format: { name: 'json', maxFileSize: '200MiB' }
        }
      }
    }
  ];

  // Archive data by running the aggregation pipeline
  await collName.aggregate(pipeline).toArray();
  console.log('Archive created!');

  // Get the 'sample_logs' collection from the 'test' database in the 'DemoCluster' service
  const collName2 = context.services.get('DemoCluster').db('test').collection('sample_logs');

  // Define the deletion query to remove archived records
  const deleteQuery = {
    timestamp: {
      $lt: start_date
    }
  };

  // Delete archived data
  const deleteResult = await collName2.deleteMany(deleteQuery);
  console.log('Deleted', deleteResult.deletedCount, 'records.');
};