/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 var openwhisk = require('openwhisk')

function main(params){
  let ow =  openwhisk()
  let resp =ow.actions.invoke({
      name:'/whisk.system/cloudant/list-documents',
      blocking:true,
      result:true,
      params:{params: {include_docs: true},bluemixServiceName: "cloudantNoSQLDB",username:"bb5297a0-0c28-4d17-b890-20d9664a960f-bluemix",host:"bb5297a0-0c28-4d17-b890-20d9664a960f-bluemix.cloudantnosqldb.appdomain.cloud",dbname:"dealerships",iamUrl:"https://iam.cloud.ibm.com/identity/token",apihost:"eu-gb.functions.cloud.ibm.com",iamApiKey:"YYK5JsJzt6yXNz5yviziW7cR7iiCAzK12jYuPyx8rFxf"}

  }).then(function(data){
      let dealerships = data.rows.map((row) => { return {
              id: row.doc.id,
              city: row.doc.city,
              state: row.doc.state,
              st: row.doc.st,
              address: row.doc.address,
              zip: row.doc.zip,
              lat: row.doc.lat,
              long: row.doc.long,
            }});
      if (!params.state){
          return {dealerships}
      }
      else{
          dealerships = dealerships.filter(item => item.st===params.state)
          return {dealerships}
      }
  })
 return resp
}