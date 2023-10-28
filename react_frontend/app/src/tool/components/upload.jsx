import React from 'react';
import {Input,Row,Col,DatePicker} from 'antd';

import BtnForm from './popup.jsx';

/* 精确年龄计算器组件 */
export default class Age extends React.Component {
  	constructor(props) {
        super(props);
        this.state = {
            output:''
        }       
    } 

    // 选择日期范围
    dateChange = (v) => {
        let now = (new Date()).toDateString();
        let msGap = (new Date(now)).getTime() - (new Date(v.toDateString())).getTime();
        let trueAge = (msGap/1000/60/60/24/365.242199).toFixed(2);
        this.setState({output: trueAge});
    }
     
    render() {          
        return (
            <div style={{marginTop:80}}> 
            <form action="http://127.0.0.1:3001/file/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name='file'/>
            </form>
            <BtnForm />  
                {/* <Row type="flex" justify="center">
                    <Col span={7}>    
                        <label style={{fontSize:14}}>您的出生日期：&nbsp;&nbsp;</label>
                        <DatePicker onChange={this.dateChange} />
                    </Col>
                    <Col span={8}>  
                        <Input addonBefore="您已在地球上存活了：" addonAfter="年" value={this.state.output} id="blue"/>
                    </Col>
                </Row> */}
            </div>
        );
    }
}

