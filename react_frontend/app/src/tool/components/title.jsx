import React from 'react';

/* 变换标题组件 */
export default class Title extends React.Component {
  	constructor(props) {
  	  	super(props);  	  	
  	}  	
    
  	render() {  		
  	  	return (
  	  	 	<h1 id="hello" style={{textAlign: 'center'}} className="animated flipInX"> {this.props.text}</h1>
  	  	);
  	}
}

