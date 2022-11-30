import ChoroplethMap from '../components/heatmap';
import Button from 'react-bootstrap/Button'
import React, {useEffect, useState} from "react";
import FilterComponent from "../components/filter";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form'

import API_URL from "../env";

var ALLBREEDS = {};

const ALL_OPTION = {label: 'All', id: -1};
const EXAMPLE_JSON = {
    "Type": {"Dog": 1, "Cat": 2, "Bird": 3, "Other": 4},
    "Age": {"Baby": 1, "Young": 2, "Adult": 3, "Senior": 4},
    "Gender": {"Female":1, "Male":2},
    "Size": {"Small":1, "Medium":2, "Large":3, "Extra Large":4},
    "Status": {"adoptable":1, "adopted":2, "hold":3},
    "Country": {"CA":1, "US":2, "MX":3},
    "Breed": {
        "Dog": {
            "Affenpinscher": 1,
            "Afghan Hound": 2,
            "Airedale Terrier": 3,
            "Akita": 4,
            "Alaskan Malamute": 5,
            "American Bulldog": 6,
        },
        "Cat": {
            "Abyssinian": 11,
            "American Bobtail": 12,
            "American Curl": 13,
            "American Shorthair": 14,
            "American Wirehair": 15,
        },
        "Bird": {
            "African Grey": 21,
            "Amazon": 22,
        },
        "Other": {
            "Alpaca": 31,
            "Barnyard": 32,
        }
    },
    "Province": {
        "CA": {
            "AB": 1,
            "BC": 2,
            "MB": 3,
            "NB": 4,
            "NL": 5,
            "NS": 6,
            "ON": 7,
        },
        "US": {
            "AL": 11,
            "AK": 12,
            "AZ": 13,
        },
        "MX": {
            "AGS": 21,
            "BCN": 22,
            "BCS": 23,
        }
    }
}

const EXAMPLE_HEATMAP_DATA = {
  "MB": 75, "SK": 43, "AB": 50, "BC": 88, "NU": 21, "NT": 43,
  "YT": 21, "ON": 19, "QC": 60, "NB": 4, "NS": 44, "NF": 38,
  "PE": 67}
//heat
function HeatMapPage(props) {
  useEffect(() => {
    fetch(API_URL+"/V0/data/entry")
    .then(res => res.json())
    .then(
        (result) => {
            //loop over parms
            setOptions(result);
        }).catch((error) => {
            if(API_URL.includes("localhost")){
                setOptions(EXAMPLE_JSON);
            }
        });
    }, []);

    function setOptions(result){
      let parms = ["Type", "Age", "Gender", "Size", "Status"]
      let setFunc = [setTypeOpt, setAgeOpt, setGenderOpt, setSizeOpt, setStatusOpt]
      let setFuncSelected = [setTypeSelected, setAgeSelected, setGenderSelected, setSizeSelected, setStatusSelected]
      
      for (let i = 0; i < parms.length; i++) {
          let parm = parms[i];
          let options = [];
          for (const [key, value] of Object.entries(result[parm])) {
              options.push({label: key, id: value});
          }
          setFunc[i]([ALL_OPTION, ...options])
          setFuncSelected[i]([ALL_OPTION])
      }
      
      parms = ["Breed"]
      setFunc = [setBreedOpt]
      setFuncSelected = [setBreedSelected]
      let cache = [ALLBREEDS]
      let dependentOptions = [typeSelected]
      
      for (let i = 0; i < parms.length; i++) {
          let parm = parms[i];
          for (const [key, value] of Object.entries(result[parm])) {
              cache[i][key] = [];
              for (const [key2, value2] of Object.entries(value)) {
                  cache[i][key].push({label: key2, id: value2, group: key});
              }
          }
          setOptionsFromCache(cache[i], dependentOptions[i], setFunc[i], setFuncSelected[i], true)
      }
      
  }
  
  function setOptionsFromCache(cache, options, setOptions, setSelected, setup){
      if(options.length === 0 && !setup){
          setOptions([]);
          setSelected([]);
          return;
      }
      else if((options.length === 1 && options[0].id === ALL_OPTION.id) || setup){
          let allOptions = [];
          for (const [key, value] of Object.entries(cache)) {
              allOptions.push(...value);
          }
          setOptions([ALL_OPTION, ...allOptions]);
          setSelected([ALL_OPTION]);
          return;
      }
      let newOptions = [];
      for (let i = 0; i < options.length; i++) {
          const option = options[i].label;
          newOptions = [...newOptions, ...cache[option]];
      }
      setOptions([ALL_OPTION, ...newOptions]);
      setSelected([ALL_OPTION]);
  }
  const [typeOpt, setTypeOpt] = useState([])
  const [typeSelected, setTypeSelected] = useState([]);
  
  const [breedOpt, setBreedOpt] = useState([])
  const [breedSelected, setBreedSelected] = useState([]);
  
  const [statusOpt, setStatusOpt] = useState([]);
  const [statusSelected, setStatusSelected] = useState([]);
  
  const [ageOpt, setAgeOpt] = useState([]);
  const [ageSelected, setAgeSelected] = useState([]);
  
  const [genderOpt, setGenderOpt] = useState([]);
  const [genderSelected, setGenderSelected] = useState([]);
  
  const [sizeOpt, setSizeOpt] = useState([]);
  const [sizeSelected, setSizeSelected] = useState([]);
  
  const [countryOpt, setCountryOpt] = useState([{label: "Canada", id:1}]);
  const [countrySelected, setCountrySelected] = useState([{label: "Canada", id:1}]);

  function reset(){
    setTypeSelected([ALL_OPTION]);
    setStatusSelected([ALL_OPTION]);
    setAgeSelected([ALL_OPTION]);
    setGenderSelected([ALL_OPTION]);
    setSizeSelected([ALL_OPTION]);
    setToToday();
    setOptionsFromCache(ALLBREEDS, typeSelected, setBreedOpt, setBreedSelected, true)
}


let now = new Date()
now = now.toISOString().split('T')[0]
const [startdate, setStartDate] = useState(now);
const [enddate, setEndDate] = useState(now);

const setToToday = () => {
    setStartDate(now);
    setEndDate(now);
}

const [advanceSearch, setAdvanceSearch] = useState(false);
const [data, setData] = useState([]);

function selectedToArrays(selected, allOptions){
    let arr = selected.map((item) => item.id);
    if(arr.includes(ALL_OPTION.id)){
        arr = allOptions.filter((item) => item.id !== ALL_OPTION.id).map((item) => item.id);
    }
    return arr
}

function getGraphData(){
    let url = API_URL + "/V0/graph/heat";
    let params = {
        "type": selectedToArrays(typeSelected, typeOpt),
        "breed": selectedToArrays(breedSelected, breedOpt),
        "status":   selectedToArrays(statusSelected, statusOpt),
        "country": countrySelected[0].label,
        "age": selectedToArrays(ageSelected, ageOpt),
        "size": selectedToArrays(sizeSelected, sizeOpt),
        "gender": selectedToArrays(genderSelected, genderOpt),
        "dateBegin": startdate,
        "dateEnd": enddate
    }
    console.log(params)
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
    }).then((response) => {
        if (response.status === 200) {
            return response.json();
        }
        else {
            throw new Error('Something went wrong on api server!');
        }})
        .then((result) => {
          setData(set_up_heatmap_data(result));
        }).catch((error) => {
            if(API_URL.includes("localhost")){
              setData(set_up_heatmap_data(EXAMPLE_HEATMAP_DATA));
            }
        });
    }
    

  function set_up_heatmap_data(data){
    //loop over data dic
    let parsed_data = []
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        parsed_data.push([key, data[key]])
      }
    }
    return parsed_data
  }
  return (
    <>
    <Container>
    <Row>
    <h1 className="title">Heat Map Visualizer</h1>
    </Row>
    <Row>
    <Col>
    <FilterComponent
    options={typeOpt}
    selectedValue={typeSelected}
    setSelectedValue={setTypeSelected}
    onChange={[setOptionsFromCache, ALLBREEDS, setBreedOpt, setBreedSelected]}
    title={"Type"}/>
    </Col>
    <Col>
    <FilterComponent
    options={breedOpt}
    selectedValue={breedSelected}
    setSelectedValue={setBreedSelected}
    groupBy={true}
    title={"Breed"}/>
    </Col>
    <Col>
    <FilterComponent
    options={statusOpt}
    selectedValue={statusSelected}
    setSelectedValue={setStatusSelected}
    title={"Status"}/>
    </Col>
    </Row>
    <Row className="rowDiv">
    <Col>
    <strong>From</strong>
    <Form.Control
    type="date"
    name="datepic"
    placeholder="DateRange"
    max={enddate}
    value={startdate}
    onChange={(e) => setStartDate(e.target.value)}/>
    </Col>
    <Col>
    <strong>To</strong>
    <Form.Control
    type="date"
    name="datepic"
    placeholder="DateRange"
    value={enddate}
    min={startdate}
    onChange={(e) => setEndDate(e.target.value)}/>
    </Col>
    <Col style={{position: "relative"}}>
    <Button variant="outline-primary" onClick={setToToday} style={{position: "absolute", bottom: "0"}}>Today</Button>
    </Col>
    </Row>
    <Row>
    {advanceSearch ?
        <strong className="AdvanceSearch" onClick={() => {
            setAdvanceSearch(false)}}>Advance Search &#8964;</strong> :
            <strong className="AdvanceSearch" onClick={() => {
                setAdvanceSearch(true)}}>Advance Search &#8963;</strong>}
                
                </Row>
                {advanceSearch && <Row className="rowDiv">
                <Col>
                <FilterComponent
                options={ageOpt}
                selectedValue={ageSelected}
                setSelectedValue={setAgeSelected}
                title={"Age"}/>
                </Col>
                <Col>
                <FilterComponent
                options={genderOpt}
                selectedValue={genderSelected}
                setSelectedValue={setGenderSelected}
                title={"Gender"}/>
                </Col>
                <Col>
                <FilterComponent
                options={sizeOpt}
                selectedValue={sizeSelected}
                setSelectedValue={setSizeSelected}
                title={"Size"}/>
                </Col>
                </Row>}
                <Row className="rowDiv">
                <Col>
                <FilterComponent
                options={countryOpt}
                selectedValue={countrySelected}
                setSelectedValue={setCountrySelected}
                title={"Country"}
                single={true}/>
                </Col>
                </Row>
                <Row>
                <Button variant="primary" 
                style={{width: "100px", margin: "10px"}}
                onClick={getGraphData}>Generate</Button>
                <Button 
                variant="primary" 
                style={{width: "100px", margin: "10px"}}
                onClick={reset}>&#x21bb; Reset </Button>
                </Row>
                <Row>
                {!props.test && <ChoroplethMap data={data}/>}
                </Row>
                </Container>
                </>
  )
}

export default HeatMapPage