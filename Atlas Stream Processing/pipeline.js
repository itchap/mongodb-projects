pipeline = [
  {
    $source: {
      connectionName: "homeKafka",  // your Kafka source connection
      topic: "logs"
    }
  },
  {
    $match: {
      // example filter: only emit login actions
      action: "login"
    }
  },
  {
    $emit: {
      connectionName: "DemoCluster",  // your Atlas cluster connection name
      collection: "logs_merged",
      database: "cyberstream"
    }
  }
]