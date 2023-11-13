import React from 'react';
import {Tabs} from 'antd';

import './tool.less';

// 引入各部分组件
import Upload from './components/upload.jsx';
import Editor from './components/editor.jsx';
import Title from './components/title.jsx';
// 引入 新建广告系列按钮 组件
// import Options from './components/options';

const TabPane = Tabs.TabPane;

/*简介父组件*/
export default class tool extends React.Component {
    render() {
        return (
            
            <div>
                <Title text="Code Audit Tool For PHP"/>
                {/* <Options/> */}
                <Tabs defaultActiveKey="1">
                    <TabPane tab="FileUpload" key="1"><Upload /></TabPane>
                    <TabPane tab="CodeInput" key="2"><Editor /></TabPane>
                </Tabs>   
                          
            </div>
            
        )
    }    
}