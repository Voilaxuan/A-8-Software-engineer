import React from 'react';
import {Tabs} from 'antd';

// 引入各部分组件
// import Hello from './components/hello.jsx';
// import Timer from './components/timer.jsx';
// import Age from './components/age.jsx';
// import Salary from './components/salary.jsx';
// import House from './components/house.jsx';
// import Bmi from './components/bmi.jsx';

import './tool.less';

const TabPane = Tabs.TabPane;

/*简介父组件*/
export default class tool extends React.Component {
    render() {
        return (
            <div>
                <Hello text="Code Audit Tool For PHP"/>
                <Timer />
                <Tabs defaultActiveKey="1">
                    <TabPane tab="FileUpload" key="1"><Age /></TabPane>
                    <TabPane tab="CodeInput" key="2"><Salary /></TabPane>
                    
                </Tabs>               
            </div>
        )
    }    
}
