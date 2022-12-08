import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import React, {useState, useEffect} from 'react';

import "./navbar.css";


function NavBar(props) {
    const [selected, setSelected] = useState("");
    
    useEffect(() => {
        let visualization = window.location.href.split("/").pop()
        setSelected(visualization);
        if(!visualization){
            setSelected("heatmap")
        }
    }, []);
    
    return (
        <>
        <Navbar bg="light" className="header">
        <Container>
        <Navbar.Brand className='Brand'>&#128062; Pet Spot</Navbar.Brand>
        {/* <Nav className="justify-content-end">
        <Nav.Link href="/about" className={selected==="about text"? "navbar-selected":"text"}>About</Nav.Link>
        </Nav> */}
        </Container>
        </Navbar>
        
        <Navbar bg="light" className="header">
        <Container>
        <Nav >
        <Nav.Link 
        className={"navbar-component "+(selected==="heatmap"?'navbar-selected text': 'text')} 
        href="/heatmap"
        onSelect={()=> {setSelected("heatmap");}}
        >Heat Map</Nav.Link>
        {/* <Nav.Link 
        className={"navbar-component componet-border "+(selected==="linegraph"?'navbar-selected text': 'text')} 
        href="/linegraph"
        onSelect={()=> {setSelected("linegraph");}}
        >Line Graph</Nav.Link> */}
        <Nav.Link 
        className={"navbar-component componet-border "+(selected==="piechart"?'navbar-selected text': 'text')}
        href="/piechart"
        onSelect={()=> {setSelected("piechart");}}
        >Pie Chart</Nav.Link>
        </Nav>
        </Container>
        </Navbar>
        
        </>
        )
    }
    
    export default NavBar