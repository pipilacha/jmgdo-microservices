const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const fs = require('fs');

const { URLSearchParams } = require('url');
global.URLSearchParams = URLSearchParams;


let rawdata = fs.readFileSync('UScities.json');
let USCities = JSON.parse(rawdata);

// GraphQL schema
let schema = buildSchema(`
    type Query {
        city(name: String): City
        /* get the city with the name Miami, return city and state fields
        {
            city (name:"Miami"){
                city
                state
            }
        }
        */
        cities(state: String): [City]
        /* get the cities where state == Ohio, returns city and state fields
            not passing state:"Ohio" returns all the cities
        {
            cities (state:"Ohio"){
                city
                state
            }
        }
        */
    },
    type City { //model of the object, only returns attributes defines here
        city: String
        state: String
    }
`);

let getCity = function(args) { 
    let name = args.name;
    return USCities.filter(city => {
        return city.city == name;
    })[0];
}

let getCities = function(args) {
    if (args.state) {
        let state = args.state;
        return USCities.filter(city => city.state === state);
    } else {
        return USCities;
    }
}

var root = { //maps the functions to the queries
    city: getCity,
    cities: getCities
};

// Create an express server and a GraphQL endpoint
var app = express();
app.use('/graphql', graphqlHTTP({
    schema: schema,
    rootValue: root, //mapped functions with queries
    graphiql: true
}));

app.get('/', (req, res) => {
    res.send("Copy the URL from the address-bar, to paste in Postman to use GraphQL")
  })
  
app.listen(4000, () => console.log('Express GraphQL Server Now Running On port 4000/graphql'));
