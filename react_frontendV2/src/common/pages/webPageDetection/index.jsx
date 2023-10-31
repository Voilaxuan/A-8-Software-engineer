import React from "react"
import './index.less'
import {Button, Form, Icon, Input, Table} from "antd"

class webPageDetectionModal extends React.Component{
    // eslint-disable-next-line no-useless-constructor
    constructor(props) {
        super(props)
    }

    submit = () =>{
        console.log('test')
    }

    render() {
        const dataSource = [{
            key: '1',
            function: 'sql injection',
            name: 'target_urllist',
            example: '[\'https://www.google.com/mapshttps://support.google.com/maps/?hl=zh-TW&authuser=0&p=no_javascript\']'
        }, {
            key: '2',
            function: 'Home page probe ip',
            name: 'iplist',
            example: '[\'19.144331.765317.5996321632\', \'3216.496431.977416.987531\', \'30.516616.541128.8215162716\', \'1827.467118.992729.702420\', \'1.9.0.4\']'
        },{
            key: '3',
            function: 'Web directory blasting',
            name: 'collect_dirs',
            example: ''
        },{
            key: '4',
            function: 'Common port detection',
            name: 'collect_ports',
            example: '[\'[-]21/tcp closed\', \'[-]22/tcp closed\', \'[-]23/tcp closed\', \'[-]25/tcp closed\', \'[-]53/tcp closed\', \'[-]80/tcp closed\', \'[-]389/tcp closed\', \'[-]8080/tcp closed\', \'[-]1433/tcp closed\', \'[-]2375/tcp closed\', \'[-]3389/tcp closed\', \'[-]6379/tcp closed\', \'[-]11211/tcp closed\', \'[-]27017/tcp closed\']'
        },{
            key: '5',
            function: 'Subdomain burst',
            name: 'subdomain',
            example: ''
        },]

        const columns = [{
            title: 'function',
            dataIndex: 'function',
            key: 'function',
        }, {
            title: 'name',
            dataIndex: 'name',
            key: 'name',
        }, {
            title: 'example',
            dataIndex: 'example',
            key: 'example',
        }]
        const { getFieldDecorator } = this.props.form

        const formItemLayout =
            {
                labelCol: { span: 10 },
                wrapperCol: { span: 14 },
            };

        const buttonItemLayout =
            {
                wrapperCol: { span: 14, offset: 4 },
            };
        return (
          <div>
              <h1 className='center'>TDScanner</h1>
              <Form name="url">
                  <Form.Item>{getFieldDecorator('urlAddress', {
                      rules: [{ required: true, message: 'Please input your url!' }],
                  })(
                      <Input
                          prefix={<Icon type="global" />}
                          placeholder="请输入网址"
                      />,
                  )}
                  </Form.Item>
              </Form>
              <Button type="primary" htmlType="submit" onClick={this.submit}>
                  Submit
              </Button>
              <Table columns={columns} dataSource={dataSource} />
          </div>


        )
    }
}
const webPageDetection = Form.create()(webPageDetectionModal)
export default webPageDetection