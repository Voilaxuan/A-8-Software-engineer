import React,{useState} from 'react';
import {Input,Row,Col,DatePicker, Button, Upload, Icon} from 'antd';

import BtnForm from './fileuploadpopup.jsx';

/* 精确年龄计算器组件 */
export default class FileUploader extends React.Component {
  	constructor(props) {
        super(props);
        this.state = {
            output:''
        }       
    }

   beforeUpload=(file)=>{
    console.log(file)
    return false;

   }
   fileinputChange = (event) =>{
    const fileData = event.target.files[0];
    console.log(fileData)
    // 获取到的文件 fileData
    // if(fileData){
    //   this.setState({ fileData, })
    //   const formdata = new FormData();
    //   formdata.append("wordType",3);
    //   formdata.append("file",fileData);
    //   this.send(formdata)
    // }
   }
   
    
     
    render() {          
        return (
            <div style={{marginTop:80}}> 


          {/* <Upload beforeUpload={(file)=>this.beforeUpload(file)} >

            <Button>
                <Icon type='upload'/>Add File

            </Button>
            <span className='upload-span'> support format: txt.......</span>
          </Upload> */}
        {/* <input id="file" type="file" onChange={this.fileinputChange}/>
        <button onClick={this.getFiles}>上传</button> */}
      
            <BtnForm/>  
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

