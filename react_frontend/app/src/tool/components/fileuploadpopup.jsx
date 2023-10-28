import React,{useState} from 'react';
import {Button,Checkbox,Select,Radio,Switch,Form,Row,Col,Icon,Modal,Input,InputNumber,Cascader,Tooltip,Upload,Divider } from 'antd';

const FormItem = Form.Item;
const RadioGroup = Radio.Group;
const CheckboxGroup = Checkbox.Group;

class AformInModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            visible: false,  
                    
        }        
    }
    // 单击确定按钮提交表单
    handleSubmit = () => {
        console.log(this.props.form.getFieldsValue());
        this.setState({ visible: false });
        let file1 = document.querySelector('#input').files[0]
        let formdata = new FormData()
        formdata.append("file", file1)  
        console.log(formdata) 
        // Axios({
        //     url:'/api/importExcel',
        //     method: 'post',
        //     headers:{'Content-Type':'multipart/form-data'},
        //     data:formdata
        // }).then(
        //     request =>{
        //         console.log(request.data)
        //     },
        //     error =>{
        //         console.log(error.data)
        //     }
        // )
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