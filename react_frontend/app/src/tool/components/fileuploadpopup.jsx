import React,{useState} from 'react';
import {Button,Checkbox,Select,Radio,Switch,Form,Row,Col,Icon,Modal,Input,InputNumber,Cascader,Tooltip,Upload,Divider } from 'antd';
import axios from 'axios';
const FormItem = Form.Item;
const RadioGroup = Radio.Group;
const CheckboxGroup = Checkbox.Group;

class AformInModal extends React.Component {

    temp_data

    constructor(props) {
        super(props);
        this.state = { 
            visible: false,  
                    
        }        
    }
    // 单击确定按钮提交表单
    handleSubmit = () => {
        this.temp_data = this.props.form.getFieldsValue()
        console.log("检测",this.temp_data);
        this.setState({ visible: false });
        console.log("打印测试",this.temp_data) 
        let fileData = new FormData()
        fileData.append('file', this.temp_data.file.raw)// 传文件
        //保护代码 避免空数据继续执行
        if(!this.temp_data){
            console.log("tempdata为空")
            return
        }
        const formdata = {
            
            entry_target_get: fileData,
            entry_ruleid_get: this.temp_data.specialRule,
            entry_secret_get: this.temp_data.secretName,
            get_format: this.temp_data.logName,
            entry_logname_get: this.temp_data.logName,
          };
        console.log("formdata",formdata)
        axios({
            url:'/api/importExcel',//
            method: 'post',
            // data:formdata
            data:formdata
        }).then(
            request =>{
                console.log("requset"+request.data)
            },
            error =>{
                console.log("error"+ error)
            }
        )
    }
    // 弹出框设置
    showModal = () => {
        this.setState({ visible: true });
    }    
    handleCancel = (e) => {
        this.setState({ visible: false });
    }  

    render() {
        const formItemLayout = {
            labelCol: { span: 6 },
            wrapperCol: { span: 16 },
        };
        
        // const uploadProps={
        //     showUploadList: true,
        //     beforeUpload:file=>{
        //         console.log(file)
        //         return false;
        //     },
            
        // };

        const { getFieldProps } = this.props.form;
        const plainOptions = ['csv', 'xml'];
        const defaultCheckedList = ['csv'];
        const ShowField=true;

        return (
            <div>
                <Button type="primary" onClick={this.showModal} size="large">New Detection</Button>
                <Modal title="New Detection" visible={this.state.visible} onOk={this.handleSubmit} onCancel={this.handleCancel}>
                    <Form horizontal>
                    <FormItem {...formItemLayout} label="LogName：">
                            <Input type="text" {...getFieldProps('logName')}/>
                        </FormItem>
                        <FormItem {...formItemLayout} label="Special Rule：">
                            <Input type="text" {...getFieldProps('specialRule')}/>
                        </FormItem>
                      
                         <Form.Item {...formItemLayout} label="Result Format：">
                         <CheckboxGroup options={plainOptions} />
                                   
                          
                        </Form.Item>
                        <FormItem {...formItemLayout} label="Secret Name：">
                            <Input type="text" {...getFieldProps('secretName')}/>
                        </FormItem>

                    {ShowField&&(
                        <FormItem {...formItemLayout} label="File：">
                            {/* <Upload >
                            <Button>
                                <Icon type="upload" />Upload File
                            </Button>
                            </Upload> */}
                            <Input type="file" {...getFieldProps('file')}/>
                        </FormItem>)}
                        {/* <FormItem {...formItemLayout} label="Upload File：">
                            <Input type="file" {...getFieldProps('fileName')}/>
                        </FormItem> */}
                        {/* <FormItem {...formItemLayout} label="ConFirm：">
                        <input type="submit" value="Start Detection"/>
                        </FormItem>                */}
                    </Form>
                </Modal>
            </div>
        )
    }
}

let Btnform = Form.create()(AformInModal);
export default Btnform;