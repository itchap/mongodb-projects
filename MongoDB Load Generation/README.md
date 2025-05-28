# Generate load

### Set up the POC Driver
cd ~/Documents/GitHub/POCDriver/bin
connStr="mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/?retryWrites=true"
connStr="mongodb+srv://admin:NokiaN900@serverlessinstance0.6ky25.mongodb.net/?retryWrites=true"
connStr="mongodb://admin:NokiaN900@server01:27018/?retryWrites=true"
connStr="mongodb+srv://itchap:NokiaN900@production.tau52.mongodb.net/?retryWrites=true"

### Ingest Rate Performance
##### 1KB inserted records
##### 10KB inserted records
java -jar POCDriver.jar -c $connStr -t 4 -e -d 600 -f 234 -a 20:20 --depth 2 -x 6
##### 50KB inserted records
java -jar POCDriver.jar -c $connStr -t 4 -e -d 600 -f 1692 -a 10:10 --depth 2 -x 8

### Realtime load Generation
java -jar POCDriver.jar -c $connStr -k 20 -i 10 -u 10 -b 20


### Slow Running Queries
cd /Users/itchap/Documents/GitHub/mdb-slow-running-queries
./run-slow-queries.sh mongodb+srv://democluster.0wrhw.mongodb.net/ itchap NokiaN900
./run-slow-queries.sh mongodb+srv://serverlessinstance0.6ky25.mongodb.net/myFirstDatabase itchap NokiaN900
./run-slow-queries.sh "mongodb://server01:27018/?authSource=admin" admin NokiaN900
./run-slow-queries.sh mongodb+srv://production.tau52.mongodb.net/ itchap NokiaN900


### Performance Advisor queries
cd /Users/itchap/Documents/GitHub/pov-proof-exercises/proofs/25
mgeneratejs CustomerSingleView.json -n 1000000 | mongoimport --uri "mongodb+srv://itchap:NokiaN900@democluster.0wrhw.mongodb.net/test" --collection customers --numInsertionWorkers=10
mgeneratejs CustomerSingleView.json -n 1000000 | mongoimport --uri "mongodb://admin:NokiaN900@server01:20018/test?authSource=admin" --collection customers --numInsertionWorkers=10
mgeneratejs CustomerSingleView.json -n 1000000 | mongoimport --uri "mongodb+srv://itchap:NokiaN900@production.tau52.mongodb.net/test" --collection customers --numInsertionWorkers=10


mongosh "mongodb://server01:27018/test?authSource=admin" --username admin
mongosh "mongodb+srv://democluster.0wrhw.mongodb.net/test" --apiVersion 1 --username itchap
mongosh "mongodb+srv://production.tau52.mongodb.net/test" --apiVersion 1 --username itchap


for (i=1; i<=10000; i++) {
   start = new Date().getTime();
   db.customers.updateOne({
      'region': i,
      'address.state': 'UT',
      'policies': {$elemMatch: {'policyType': 'life', 'insured_person.smoking': true}},
      'yob': {$gte: ISODate('1990-01-01'), $lte : ISODate('1990-12-12')},
      'gender': 'Female'
   },
   { $set: { "policies.$[elem].risk" : 300 } },
   {
      multi: true,
      arrayFilters: [ { "elem.policyType": "life" } ]
   });
   print(i, ". time (ms): ", ((new Date().getTime())-start));
}
