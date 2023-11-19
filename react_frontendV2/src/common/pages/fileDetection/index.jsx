import React from 'react'
import axios from 'axios'
import './index.less'
import { Button, Form, Icon, Input, Table, Modal, Checkbox } from 'antd'
const baseURL = 'http://20.2.73.68:5003'
class fileDetectionModal extends React.Component {
  // eslint-disable-next-line no-useless-constructor
  temp_data

  constructor(props) {
    super(props)
    this.state = {
      visible: false,
      selectedFile: null,
      selectedFileOption: '', // 初始选中值为空
      fileOptions: []
    }
  }
  componentDidMount() {
    this.fetchFileOptions()
  }
  fetchFileOptions = () => {
    fetch(baseURL + '/nogetfilelist', {
      method: 'post'
    }) // 替换为实际的API URL
      .then(response => response.json())
      .then(data => {
        if (data.status === 1) {
          const newFileOptions = data.fileslist
          this.setState({ fileOptions: newFileOptions }, () => {
            // 确保有选项可选
            if (newFileOptions.length > 0) {
              const lastOptionValue = newFileOptions[newFileOptions.length - 1].filevalue
              this.setState({ selectedFileOption: lastOptionValue })
            }
          })
          console.log(data.fileslist)
        }
      })
      .catch(error => console.error('Error fetching code vul options:', error))
  }

  handleFileChange = event => {
    console.log('changchangechange')
    this.setState({ selectedFile: event.target.files[0] })
  }

  handleUpload = () => {
    const { selectedFile } = this.state
    if (!selectedFile) {
      console.log('No file selected')
      return
    }
    console.log('uploadinging', selectedFile)
    const formData = new FormData()
    formData.append('file', selectedFile)

    fetch(baseURL + '/noupload', {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then(data => {
        console.log('File uploaded successfully:', data)
        console.log('filename', data.filepath)
        //更新选项
        this.fetchFileOptions()

        // 处理上传成功逻辑
      })
      .catch(error => {
        console.error('Error uploading file:', error)
        // 处理错误逻辑
      })
  }
  handleSelectOptionChange = event => {
    // 更新状态以反映用户选择的文件选项
    this.setState({ selectedFileOption: event.target.value })
  }

  handleCodeVulCheck = () => {
    // Get the selected option value
    var selectedOption = document.getElementById('fileSelect').value

    console.log('path', selectedOption)
    // Make a POST request to /dovulfetch
    fetch(baseURL + '/novuldetect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        // filepath: selectedOption
        filepath: '1b67c72a-695f-4c46-ae75-6ecfb4027f84'
        // "第35次提交: /20f9adbf-3f05-4fc5-ac0d-7bcfad583004/"
      })
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response data
        console.log(data)
        // Check if the response status is 1 and data is "OK"
        if (data.status === 1 && data.data === 'OK') {
          fetch(baseURL + '/novulfetch', {
            method: 'POST',
            body: JSON.stringify({
              // filepath: selectedOption
              filepath: '1b67c72a-695f-4c46-ae75-6ecfb4027f84'
            })
          })
            .then(response => response.json())
            .then(data => {
              // Handle the response data
              console.log(data)
              // Check if the response status is 1 and data is "OK"
              //alert(data.toString());
              var jsonString = JSON.stringify(data)
              alert('Code Vul Check Success!')
              // var nameElement = document.getElementById('resulttext');
              // nameElement.innerHTML = jsonString;
            })
            .catch(error => {
              // Handle errors
              console.error('Error:', error)
            })
        } else {
          alert('Code Vul Check failed!')
        }
      })
      .catch(error => {
        // Handle errors
        console.error('Error:', error)
      })
  }

  // 单击确定按钮提交表单
  handleSubmit = () => {
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
      entry_target_get: fileData,
      entry_ruleid_get: this.temp_data.specialRule,
      entry_secret_get: this.temp_data.secretName,
      get_format: this.temp_data.logName,
      entry_logname_get: this.temp_data.logName
    }
    console.log('formdata', formdata)
    fetch(baseURL + '/nogetfilelist', {
      method: 'post'
      // data:formdata
      // data: fileData,
      // withCredentials:true,
    }).then(
      response => {
        console.log('response', response.json())
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
    const ShowField = true

    return (
      <div>
        <Button type="primary" onClick={this.showModal} size="large">
          New File Detection
        </Button>
        <Modal
          title="New Detection"
          visible={this.state.visible}
          onOk={this.handleCodeVulCheck}
          onCancel={this.handleCancel}
        >
          <Form horizontal>
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
              <Form.Item label="File：" {...formItemLayout}>
                <Input type="file" onChange={this.handleFileChange} />
                <Button type="primary" onClick={this.handleUpload}>
                  Upload File
                </Button>
              </Form.Item>
            )}
            {/* <FormItem {...formItemLayout} label="Upload File：">
                            <Input type="file" {...getFieldProps('fileName')}/>
                        </FormItem> */}
            {/* <FormItem {...formItemLayout} label="ConFirm：">
                        <input type="submit" value="Start Detection"/>
                        </FormItem>                */}
            <Form.Item {...formItemLayout} label="File List：">
              <select
                id="fileSelect"
                value={this.state.selectedFileOption}
                onChange={this.handleSelectOptionChange}
              >
                {this.state.fileOptions.map(option => (
                  <option key={option.filevalue} value={option.filevalue}>
                    {option.filename}
                  </option>
                ))}
              </select>
            </Form.Item>
          </Form>
        </Modal>
      </div>
    )
  }
}
const fileDetection = Form.create()(fileDetectionModal)
export default fileDetection
