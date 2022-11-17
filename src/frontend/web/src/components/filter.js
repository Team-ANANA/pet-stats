import { Multiselect } from 'multiselect-react-dropdown';

function FilterComponent(props){
// props.options = [{name: 'Srigar', id: 1},{name: 'Sam', id: 2}]
// let options = props.options;
// if(!props.single){
//  options = [{label: "All", id: 0}, ...props.options]
// }
let options = props.options;

const onSelect = (list, item) => {
    if(item.label === "All"){
        //props.setSelectedValue(options)
        props.setSelectedValue([item])
    } else {
        list = list.filter((item) => item.label !== "All")
        props.setSelectedValue(list)
    }
    if(props.onChange){
        props.onChange[0](props.onChange[1], list, props.onChange[2], props.onChange[3], false)
    }
}

const onRemove = (list, item) => {
    if(item.label === "All"){
        props.setSelectedValue([])
    } else {
        props.setSelectedValue(list)
    }
}

return (   
    <>
    <strong>{props.title}</strong>
<Multiselect
    options={options} // Options to display in the dropdown
    selectedValues={props.selectedValue} // Preselected value to persist in dropdown
    onSelect={onSelect} // Function will trigger on select event
    onRemove={onRemove} // Function will trigger on remove event
    displayValue="label" // Property name to display in the dropdown options
    showCheckbox={true}
    avoidHighlightFirstOption={true}
    singleSelect={props.single}
    groupBy={props.groupBy ? "group": ""}
    style={{multiselectContainer: {width: (props.width?props.width+"px":'200px')}}}
    />
    </>)
}

export default FilterComponent