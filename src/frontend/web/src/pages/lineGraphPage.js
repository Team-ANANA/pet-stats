import React, {useEffect, useState} from "react";
import LineGraph from "../components/linegraph"
import API_URL from "../env";

function LineGraphPage() {

    
    return (
      <>
      <LineGraph data={ [
            {"date": "2009-04-28", "value": "135.98", "sort": "cat"},
            {"date": "2011-05-28", "value": "15.9338", "sort": "dog"},
            {"date": "2013-09-22", "value": "38", "sort": "dog"},
            {"date": "2014-06-28", "value": "90", "sort": "cat"}
        ]}/>
    </>
    )
  }
  
  export default LineGraphPage