/**
 * MongoDB Cluster Statistics Aggregator Script
 * 
 * This script retrieves statistics for each database in a MongoDB cluster,
 * calculates cumulative values, and outputs a summary of the total data,
 * storage, and index sizes across all databases. Additionally, it provides
 * information about the cluster, including MongoDB version, uptime, current
 * connections, replica set details, opcounters, and document metrics.
 */

// Function to format bytes into a human-readable format
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Function to format uptime into days, hours, minutes, and seconds
function formatUptime(uptimeInSeconds) {
    const days = Math.floor(uptimeInSeconds / (60 * 60 * 24));
    const hours = Math.floor((uptimeInSeconds % (60 * 60 * 24)) / (60 * 60));
    const minutes = Math.floor((uptimeInSeconds % (60 * 60)) / 60);
    const seconds = uptimeInSeconds % 60;
    return `${days}d ${hours}h ${minutes}m ${seconds}s`;
}

// Get server status for additional information
var serverStatus = db.serverStatus();
var replicaSetStatus = rs.status();

// Output cluster information
print('\nCluster Information');
print('----------------------------------');
// Output replica set information
print('Replica Set Nodes: ' + replicaSetStatus.members.length);
print('Replica Set Name: ' + replicaSetStatus.set);
// Output server status information
print('MongoDB Version: ' + serverStatus.version);
print('Uptime: ' + formatUptime(serverStatus.uptime));
print('Current Connections: ' + serverStatus.connections.current);

// Output opcounters
print('\nOpcounters:');
for (var operation in serverStatus.opcounters) {
    print(`  ${operation}: ${serverStatus.opcounters[operation].toLocaleString()}`);
}

// Output document metrics
print('Document Metrics:');
for (var metric in serverStatus.metrics.document) {
    print(`  ${metric}: ${serverStatus.metrics.document[metric].toLocaleString()}`);
}

// Output each database size (uncompressed)
print('\nEach Database Size (uncompressed)');
print('----------------------------------');

// Get the list of databases
var databases = db.runCommand({ listDatabases: 1 }).databases;
// Sort databases based on fileSize in descending order
databases.sort(function (a, b) {
    return b.sizeOnDisk - a.sizeOnDisk;
});

// Initialize cumulative variables
var totalObjects = 0;
var totalFileSize = 0;
var totalStorageSize = 0;
var totalIndexes = 0;
var totalIndexSize = 0;
var totalCollections = 0;

// Loop through each database and output human-readable values
databases.forEach(function (database) {
    var dbName = database.name;
    db = db.getSiblingDB(dbName);

    // Get the database statistics
    var stats = db.runCommand({ dbStats: 1 });

    // Calculate average object size
    var avgObjectSize = stats.objects !== 0 ? stats.fileSize / stats.objects : 0;

    // Calculate total size (storage size + index size)
    var totalSize = stats.storageSize + stats.indexSize;

    // Update cumulative variables
    totalObjects += stats.objects;
    totalFileSize += stats.fileSize;
    totalStorageSize += stats.storageSize;
    totalIndexes += stats.indexes;
    totalIndexSize += stats.indexSize;
    totalCollections += stats.collections;

    // Output database name and size
    print(dbName + '    \t size: ' + formatBytes(stats.fileSize) + '    \tdocs: ' + stats.objects + '   \tavg doc: ' + formatBytes(avgObjectSize));
});

// Output total values for all databases
print('\nTotal Cluster Sizes');
print('----------------------------------');
print('Total Databases: ' + databases.length);
print('Total Collections: ' + totalCollections);
print('Total Objects: ' + totalObjects);
print('Total Raw Data Size: ' + formatBytes(totalFileSize));
print('Total Storage Size on Disk: ' + formatBytes(totalStorageSize));
print('Total Indexes: ' + totalIndexes);
print('Total Index Size: ' + formatBytes(totalIndexSize));
print('Total Avg Object Size: ' + formatBytes(totalFileSize / totalObjects));
print('\n\n');
