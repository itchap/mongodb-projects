# Find Query Example
database: test
collection: customers
filter by
```
{gender: "Male", region: {$gte: 627, $lte: 628}}
```

sort by
```
{firstname: 1}
```


### Group Query
Database: test
Collection: Sales

##### Match Stage
{
  date: {
    $gte: new ISODate("2014-01-01"),
    $lt: new ISODate("2015-01-01"),
  }
}

#### Group Stage
{
  _id: {
    $dateToString: {
      format: "%Y-%m-%d",
      date: "$date",
    },
  },
  totalSaleAmount: {
    $sum: {
      $multiply: ["$price", "$quantity"],
    },
  },
  averageQuantity: {
    $avg: "$quantity",
  },
  count: {
    $sum: 1,
  },
}

#### Sort Stage
{
  totalSaleAmount: -1,
}


lookup

db.orders.aggregate
[
   {
     $lookup:
       {
         from: "inventory",
         localField: "item",
         foreignField: "sku",
         as: "inventory_docs"
       }
  }
]



Geo
{
 location:
   { $near:
      {
        $geometry: { type: "Point",  coordinates: [ -73.9667, 40.78 ] },
        $minDistance: 1000,
        $maxDistance: 5000
      }
   }
}


agg

[
   {
      $geoNear: {
         near: { type: "Point", coordinates: [ -73.9667, 40.78 ] },
         spherical: true,
         query: { category: "Parks" },
         distanceField: "calcDistance"
      }
   }
]
