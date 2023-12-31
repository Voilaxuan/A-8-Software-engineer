import React from 'react'
import { Link } from 'react-router-dom'
import { Menu, Icon, Switch, Layout } from 'antd'
import { connect } from 'react-redux'
import { hot } from 'react-hot-loader/root'
import allMenu from '../utils/menu'
import Top from './header'
import Contents from './content'
import Footer from './bottom'
import './index.less'

const { SubMenu } = Menu
const { Sider } = Layout

@connect(state => ({
  router: state.router
}))
class Container extends React.Component {
  state = {
    theme: 'dark',
    collapsed: false,
    mode: 'inline'
  }

  changeTheme = value => {
    this.setState({
      theme: value ? 'dark' : 'light'
    })
  }

  toggle = () => {
    const { collapsed } = this.state
    this.setState({
      collapsed: !collapsed,
      mode: collapsed ? 'inline' : 'vertical'
    })
  }

  render() {
    const { collapsed, theme, mode } = this.state
    const { router } = this.props
    const selectedKey = router.location.pathname.split('/')[1]
    let openKey = ''
    for (const menuObj of allMenu) {
      if (menuObj.children) {
        for (const menuList of menuObj.children) {
          if (menuList.url === selectedKey) {
            openKey = menuObj.url
            break
          }
        }
      }
    }
    return (
      <Layout className="containAll">
        <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
          {theme === 'light' ? (
            <a
              href="https://github.com/Voilaxuan/A-8-Software-engineer"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Icon type="github" className="github" />
            </a>
          ) : (
            <a
              href="https://github.com/Voilaxuan/A-8-Software-engineer"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Icon type="github" className="github white" />
            </a>
          )}
          {theme === 'light' ? (
            <span className="author">SE</span>
          ) : (
            <span className="author white">SE</span>
          )}
          <Menu
            theme={theme}
            defaultOpenKeys={[openKey]}
            selectedKeys={[selectedKey]}
            className="menu"
            mode={mode}
          >
            {allMenu.map(subMenu => {
              if (subMenu.children && subMenu.children.length) {
                return (
                  <SubMenu
                    key={subMenu.url}
                    title={
                      <span>
                        <Icon type={subMenu.icon} />
                        <span>{subMenu.name}</span>
                      </span>
                    }
                  >
                    {subMenu.children.map(menu => (
                      <Menu.Item key={menu.url}>
                        <Link to={`/${menu.url}`}>{menu.name}</Link>
                      </Menu.Item>
                    ))}
                  </SubMenu>
                )
              }
              return (
                <Menu.Item key={subMenu.url}>
                  <Link to={`/${subMenu.url}`}>
                    <Icon type={subMenu.icon} />
                    <span className="nav-text">{subMenu.name}</span>
                  </Link>
                </Menu.Item>
              )
            })}
          </Menu>
          <div className="switch">
            <Switch
              checked={theme === 'dark'}
              onChange={this.changeTheme}
              checkedChildren="Dark"
              unCheckedChildren="Light"
            />
          </div>
        </Sider>
        <Layout>
          <Top toggle={this.toggle} collapsed={collapsed} />
          <Contents />
          <Footer />
        </Layout>
      </Layout>
    )
  }
}

let handleComponent = Container
// 静默刷新
if (ENABLE_DEVTOOLS) {
  handleComponent = hot(Container)
}

export default handleComponent
