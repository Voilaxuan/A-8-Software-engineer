import React from 'react'
import 'regenerator-runtime/runtime'
import './index.less'
import { Button, Form, Icon, Input, Table, Modal, Checkbox } from 'antd'

const baseURL = 'http://20.2.73.68:5003/'

import Editor from './components/editor.jsx'
class codeTextDetectionModal extends React.Component {
  // eslint-disable-next-line no-useless-constructor
  temp_data

  constructor(props) {
    super(props)
    this.state = {
      visible: false
    }
  }

  // 单击确定按钮提交表单
  handleSubmit = async () => {
    this.temp_data = this.props.form.getFieldsValue()
    console.log('检测', this.temp_data)
    this.setState({ visible: false })
    console.log('打印测试', this.temp_data)
    let fileData = new FormData()
    // fileData.append('file', this.temp_data.file.raw) // 传文件
    //保护代码 避免空数据继续执行
    if (!this.temp_data) {
      console.log('tempdata为空')
      return
    }

    const formdata = {
      // entry_target_get: fileData,
      entry_ruleid_get: this.temp_data.specialRule,
      entry_secret_get: this.temp_data.secretName,
      get_format: this.temp_data.logName,
      entry_logname_get: this.temp_data.logName
    }
    console.log('formdata', formdata)
    console.log(baseURL + 'magicsession')

    const sessionReq = await fetch(baseURL + 'magicsession', {
      method: 'get'
      // data:formdata
    }).then(
      res => {
        console.log('response', res.json())
        // return fetch.get(baseURL+"dovuldetect");
      },
      error => {
        console.log('error', error)
      }
    )

    const detectReq = await fetch(baseURL + 'dovuldetect', {
      method: 'get',
      // data:formdata
      credentials: 'include'
    }).then(
      res => {
        console.log('response', res.json())
        // return fetch.get(baseURL+"dovuldetect");
      },
      error => {
        console.log('error', error)
      }
    )
  }

  // 弹出框设置
  showModal = () => {
    this.setState({ visible: true })
  }
  handleCancel = e => {
    this.setState({ visible: false })
  }

  render() {
    const formItemLayout = {
      labelCol: { span: 6 },
      wrapperCol: { span: 16 }
    }

    // const uploadProps={
    //     showUploadList: true,
    //     beforeUpload:file=>{
    //         console.log(file)
    //         return false;
    //     },

    // };

    const { getFieldProps } = this.props.form
    const plainOptions = ['csv', 'xml']
    const defaultCheckedList = ['csv']
    const ShowField = false

    return (
      <div>
        <Editor></Editor>
        <Button type="primary" onClick={this.showModal} size="large">
          New CodeText Detection
        </Button>
        <Modal
          title="New Detection"
          visible={this.state.visible}
          onOk={this.handleSubmit}
          onCancel={this.handleCancel}
        >
          <Form horizontal>
            <Form.Item {...formItemLayout} label="TestForm">
              <Input type="text" {...getFieldProps('TestForm')} />
            </Form.Item>
            <Form.Item {...formItemLayout} label="LogName：">
              <Input type="text" {...getFieldProps('logName')} />
            </Form.Item>
            <Form.Item {...formItemLayout} label="Special Rule：">
              <Input type="text" {...getFieldProps('specialRule')} />
            </Form.Item>

            <Form.Item {...formItemLayout} label="Result Format：">
              <Checkbox.Group options={plainOptions} />
            </Form.Item>
            <Form.Item {...formItemLayout} label="Secret Name：">
              <Input type="text" {...getFieldProps('secretName')} />
            </Form.Item>

            {ShowField && (
              <Form.Item {...formItemLayout} label="File：">
                {/* <Upload >
                            <Button>
                                <Icon type="upload" />Upload File
                            </Button>
                            </Upload> */}
                <Input type="file" {...getFieldProps('file')} />
              </Form.Item>
            )}
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
const codeTextDetection = Form.create()(codeTextDetectionModal)
export default codeTextDetection
