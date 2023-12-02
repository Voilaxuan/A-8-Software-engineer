import React from 'react'
import './index.less'
import { Button, Form, Icon, Input, Table } from 'antd'
import { ajax } from '../../utils'
import 'regenerator-runtime'
import Cookies from 'js-cookie'
import map from 'react-error-overlay/lib/utils/mapper'
class webPageDetectionModal extends React.Component {
  constructor(props) {
    super(props)
  }

  storedCookie = ''
  dataSource = []
  submit = () => {
    console.log('url', this.props.form.getFieldValue('urlAddress'))
    fetch('http://20.2.73.68:5003/nourlfetch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        url: this.props.form.getFieldValue('urlAddress')
      })
    })
      .then(response => {
        console.log(response)
        return response.json()
      })
      .then(data => {
        console.log('data', data)
        console.log('target', data.message)
        if (data.message != 'something wrong') {
          console.log('json', JSON.parse(data.message))
          const messageParse = JSON.parse(data.message)
          if (messageParse.target_urllist == undefined || messageParse.target_urllist == null) {
            return
          }
          this.dataSource = [
            {
              key: '1',
              function: 'sql injection',
              name: 'target_urllist',
              example: messageParse.target_urllist
            },
            {
              key: '2',
              function: 'Home page probe ip',
              name: 'iplist',
              example: messageParse.iplist
            },
            {
              key: '3',
              function: 'Web directory blasting',
              name: 'collect_dirs',
              example: messageParse.collect_dirs
            },
            {
              key: '4',
              function: 'Common port detection',
              name: 'collect_ports',
              example: messageParse.collect_ports.join(';  ')
            },
            {
              key: '5',
              function: 'Subdomain burst',
              name: 'subdomain',
              example: messageParse.subdomain
            },
            {
              key: '6',
              function: 'Dns content',
              name: 'dns_content',
              example: String(messageParse.dns_content)
            },
            {
              key: '7',
              function: 'Different Dns',
              name: 'different_dns',
              example: messageParse.different_dsn.join(';  ')
            }
          ]
          // this.dataSource.push(new Map([['key','1'],
          //     ['function','sql injection'],
          //     ['name','target_urllist'],
          //     ['example',messageParse.target_urllist]]))
          // this.dataSource.push(new Map([['key','2'],
          //     ['function','Home page probe ip'],
          //     ['name','iplist'],
          //     ['example',messageParse.iplist]]))
          // this.dataSource.push(new Map([['key','3'],
          //     ['function','Web directory blasting'],
          //     ['name','collect_dirs'],
          //     ['example',messageParse.collect_dirs]]))
          // this.dataSource.push(new Map([['key','4'],
          //     ['function','Common port detection'],
          //     ['name','collect_ports'],
          //     ['example',messageParse.collect_ports]]))
          // this.dataSource.push(new Map([['key','5'],
          //     ['function','Subdomain burst'],
          //     ['name','subdomain'],
          //     ['example',messageParse.subdomain]]))
          console.log('this.dataSource', this.dataSource)
          this.forceUpdate()
        }
      })
  }
  submit2 = () => {
    console.log('test')
    fetch('http://20.2.73.68:5003/magicsession', {
      method: 'get'
    })
      .then(res => {
        console.log(res)
        const headers = res.headers
        console.log('headers', headers)
        console.log('cookie', headers.getSetCookie())
        this.storedCookie = headers.get('Set-Cookie')
        console.log("headers.get('Set-Cookie')", headers.get('Set-Cookie'))
        console.log('this.storedCookie', this.storedCookie)
        return res
      })
      .then(text => {
        console.log('text', text)
      })
    // ajax.fetchJSONByGet('http://20.2.73.68:5002/magicsession')
  }

  render() {
    // const dataSource = [{
    //     key: '1',
    //     function: 'sql injection',
    //     name: 'target_urllist',
    //     example: '[\'https://www.google.com/mapshttps://support.google.com/maps/?hl=zh-TW&authuser=0&p=no_javascript\']'
    // }, {
    //     key: '2',
    //     function: 'Home page probe ip',
    //     name: 'iplist',
    //     example: '[\'19.144331.765317.5996321632\', \'3216.496431.977416.987531\', \'30.516616.541128.8215162716\', \'1827.467118.992729.702420\', \'1.9.0.4\']'
    // },{
    //     key: '3',
    //     function: 'Web directory blasting',
    //     name: 'collect_dirs',
    //     example: ''
    // },{
    //     key: '4',
    //     function: 'Common port detection',
    //     name: 'collect_ports',
    //     example: '[\'[-]21/tcp closed\', \'[-]22/tcp closed\', \'[-]23/tcp closed\', \'[-]25/tcp closed\', \'[-]53/tcp closed\', \'[-]80/tcp closed\', \'[-]389/tcp closed\', \'[-]8080/tcp closed\', \'[-]1433/tcp closed\', \'[-]2375/tcp closed\', \'[-]3389/tcp closed\', \'[-]6379/tcp closed\', \'[-]11211/tcp closed\', \'[-]27017/tcp closed\']'
    // },{
    //     key: '5',
    //     function: 'Subdomain burst',
    //     name: 'subdomain',
    //     example: ''
    // },]

    const columns = [
      {
        title: 'function',
        dataIndex: 'function',
        key: 'function'
      },
      {
        title: 'name',
        dataIndex: 'name',
        key: 'name'
      },
      {
        title: 'example',
        dataIndex: 'example',
        key: 'example'
      }
    ]
    const { getFieldDecorator } = this.props.form

    const formItemLayout = {
      labelCol: { span: 10 },
      wrapperCol: { span: 14 }
    }

    const buttonItemLayout = {
      wrapperCol: { span: 14, offset: 4 }
    }
    return (
      <div>
        <h1 className="center">TDScanner</h1>
        <Form>
          <Form.Item>
            {getFieldDecorator('urlAddress', {
              rules: [{ required: true, message: 'Please input your url!' }]
            })(
              <Input
                prefix={<Icon type="global" />}
                placeholder="请输入网址 http://www.xxx.com 格式"
              />
            )}
          </Form.Item>
        </Form>
        <Button type="primary" htmlType="submit" onClick={this.submit}>
          Submit
        </Button>
        {/*<Button type="primary" htmlType="submit" onClick={this.submit2}>*/}
        {/*    Submit2*/}
        {/*</Button>*/}
        <Table columns={columns} dataSource={this.dataSource} />
      </div>
    )
  }
}
const webPageDetection = Form.create()(webPageDetectionModal)
export default webPageDetection
