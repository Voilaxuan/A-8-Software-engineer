import React from 'react';
import {Button,Checkbox,Select,Radio,Switch,Form,Row,Col,Icon,Modal,Input,InputNumber,Cascader,Tooltip, CheckboxGroup } from 'antd';

const FormItem = Form.Item;
const RadioGroup = Radio.Group;

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
        const areaData = [{
            value: 'audi',
            label: '奥迪',
            children: [{
                value: 'a6',
                label: 'AudiA6',                
            },{
                value: 'a8',
                label: 'AudiA8',                
            }],
        }];
        const { getFieldProps } = this.props.form;

        return (
            <div>
                
                
                {/* <Button type="primary" onClick={this.showModal} size="large">新建广告系列</Button> */}
                {/* <Modal title="新建广告系列" visible={this.state.visible} onOk={this.handleSubmit} onCancel={this.handleCancel}> */}
                    <Form horizontal>
                        <FormItem {...formItemLayout} label="LogName：">
                            <Input type="text" {...getFieldProps('logName')}/>
                        </FormItem>
                        <FormItem {...formItemLayout} label="Special Rule：">
                            <Input type="text" {...getFieldProps('specialRule')}/>
                            {/* <Cascader options={areaData}  {...getFieldProps('specialRule')}/> */}
                        </FormItem>
                        {/* <FormItem {...formItemLayout} label="Result Format：">
                            <RadioGroup defaultValue="csv" size="large" {...getFieldProps('resultFormat')}>
                                <Radio key="a" value="csv">Save as csv</Radio>
                                <Radio key="b" value="xml">Save as xml</Radio>
                            </RadioGroup>
                        </FormItem> */}
                         <Form.Item {...formItemLayout} label="Result Format：">
                            
                                    <Checkbox key="a" value="csv">Save as csv</Checkbox>
                                    <Checkbox key="b" value="xml">Save as xml</Checkbox>
                          
                        </Form.Item>
                        <FormItem {...formItemLayout} label="Secret Name：">
                            <Input type="text" {...getFieldProps('secretName')}/>
                        </FormItem>
                        <FormItem {...formItemLayout} label="Upload File：">
                            <Input type="file" {...getFieldProps('fileName')}/>
                        </FormItem>
                        <FormItem {...formItemLayout} label="ConFirm：">
                        <input type="submit" value="Start Detection"/>
                        </FormItem>
                        {/* <FormItem {...formItemLayout} 
                            label={
                                <span>匀速投放{' '} 
                                    <Tooltip title="开启“匀速投放”后，系统会智能控制广告的投放速度，让您的广告预算在投放时段内较为平稳的消耗，但您可能会错失部分目标客户。关闭“匀速投放”后，广告会以较快的速度尽可能获得更多的曝光，但可能导致您的预算在短时间内消耗尽。">
                                        <Icon type="question-circle-o" />
                                    </Tooltip> ：
                                </span>
                            }>
                            <Switch checkedChildren="开" unCheckedChildren="关" {...getFieldProps('line')}/>
                        </FormItem>                         */}
                    </Form>
                {/* </Modal> */}
            </div>
        )
    }
}

let Btnform = Form.create()(AformInModal);
export default Btnform;