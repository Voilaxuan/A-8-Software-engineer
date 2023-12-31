import React from 'react'
import axios from 'axios'
import './index.less'
import { Button, Form, Icon, Input, Table, Modal, Checkbox } from 'antd'
import 'highlight.js/styles/default.css'
import hljs from 'highlight.js'

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
      fileOptions: [],
      fileContent: '',
      jsonResult: '',
      highlightedLine: null
    }
  }
  componentDidMount() {
    this.fetchFileOptions()
    hljs.highlightAll()
  }
  componentDidUpdate() {
    // 当组件更新时也高亮代码块
    hljs.highlightAll()
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

    const file = event.target.files[0]
    if (!file) {
      return
    }

    const reader = new FileReader()
    reader.onload = this.handleShowFile
    reader.readAsText(file) // 读取文件内容为文本
  }
  handleShowFile = event => {
    const fileContent = event.target.result
    this.setState({ fileContent })
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
              var nameElement = document.getElementById('resulttext')
              nameElement.innerHTML = jsonString

              this.setState({ jsonResult: jsonString })

              this.setState({ fileContent: this.renderJsonResultWithFile() })

              // var codeElement = document.getElementById('code-render');

              // codeElement.innerHTML=this.renderJsonResultWithFile();
              // alert('Code Vul Check Success!')
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
    this.setState({ visible: false })
  }

  parseJsonResult = () => {
    try {
      const result = JSON.parse(this.state.jsonResult)
      const firstKey = Object.keys(result.data)[0]
      const vulnerabilitiesData = result.data[firstKey]
      const vulnerabilities = vulnerabilitiesData.vulnerabilities.vul

      // 创建一个以行号为键的对象，存储每行的分析内容
      const highlights = vulnerabilities.reduce((acc, vul) => {
        acc[vul.line_number.trim()] = vul.analysis
        return acc
      }, {})
      console.log(highlights)
      this.setState({ highlightedLine: highlights })

      return highlights
    } catch (error) {
      console.error('Error parsing JSON result:', error)
    }
    return {}
  }

  renderJsonResultWithFile = () => {
    this.parseJsonResult()
    const { fileContent, highlightedLine } = this.state
    const lines = fileContent.split('\n')

    console.log('highlightedLine', highlightedLine)
    return lines.map((line, index) => {
      const lineNumber = (index + 1).toString()
      const highlightInfo = highlightedLine[lineNumber] // 清除可能的空格
      console.log('lineNumber.trim()', lineNumber.trim())
      console.log('highlightInfo', highlightInfo)
      const isHighlighted = Boolean(highlightInfo) // 如果行号在 highlightedLine 中，则为 true
      const lineClass = isHighlighted ? 'highlighted' : ''
      const title = isHighlighted ? highlightInfo : '' // 可以是分析内容或其他信息
      console.log('lineClass', lineClass)
      return (
        <div key={lineNumber} className={`code-line ${lineClass}`} title={title}>
          {line}
        </div>
      )
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
        <div className="file-content">
          <h3>File Content:</h3>
          <pre>
            <code className="php" id="code-render">
              {this.state.fileContent}
            </code>
          </pre>
        </div>

        <section>
          <h2>Results</h2> <button id="clearresultcontentBtn">Clear Result Content</button>
          <table border="1">
            <tr>
              <td>Result Form</td>
            </tr>
            <tr>
              <td id="resulttext"></td>
            </tr>
          </table>
        </section>
      </div>
    )
  }
}
const fileDetection = Form.create()(fileDetectionModal)
export default fileDetection
