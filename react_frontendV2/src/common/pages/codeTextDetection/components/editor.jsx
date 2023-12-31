import React, { Component } from 'react'
import { Row, Col, Card } from 'antd'
import { Editor } from 'react-draft-wysiwyg'
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css'

const rawContentState = {
  entityMap: {
    '0': {
      type: 'IMAGE',
      mutability: 'MUTABLE',
      data: { src: 'http://i.imgur.com/aMtBIep.png', height: 'auto', width: '100%' }
    }
  },
  blocks: [
    {
      key: '9unl6',
      text: '',
      type: 'unstyled',
      depth: 0,
      inlineStyleRanges: [],
      entityRanges: [],
      data: {}
    },
    {
      key: '95kn',
      text: ' ',
      type: 'atomic',
      depth: 0,
      inlineStyleRanges: [],
      entityRanges: [{ offset: 0, length: 1, key: 0 }],
      data: {}
    },
    {
      key: '7rjes',
      text: '',
      type: 'unstyled',
      depth: 0,
      inlineStyleRanges: [],
      entityRanges: [],
      data: {}
    }
  ]
}

export default class wysiwyg extends Component {
  state = {
    editorContent: undefined,
    contentState: rawContentState,
    editorState: ''
  }

  onEditorChange = editorContent => {
    this.setState({
      editorContent
    })
  }

  clearContent = () => {
    this.setState({
      contentState: ''
    })
  }

  onContentStateChange = contentState => {
    console.log('contentState', contentState)
  }

  onEditorStateChange = editorState => {
    this.setState({
      editorState
    })
  }

  imageUploadCallBack = file =>
    new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open('POST', 'https://api.imgur.com/3/image')
      xhr.setRequestHeader('Authorization', 'Client-ID 8d26ccd12712fca')
      const data = new FormData()
      data.append('image', file)
      xhr.send(data)
      xhr.addEventListener('load', () => {
        const response = JSON.parse(xhr.responseText)
        resolve(response)
      })
      xhr.addEventListener('error', () => {
        const error = JSON.parse(xhr.responseText)
        reject(error)
      })
    })

  render() {
    const { editorContent, editorState } = this.state
    return (
      <div>
        <Row gutter={16}>
          <Col span={24}>
            <div className="cloud-box">
              <Card title="富文本编辑器" bordered>
                <Editor
                  editorState={editorState}
                  toolbarClassName="home-toolbar"
                  wrapperClassName="home-wrapper"
                  editorClassName="home-editor"
                  onEditorStateChange={this.onEditorStateChange}
                  toolbar={{
                    history: { inDropdown: true },
                    list: { inDropdown: true },
                    textAlign: { inDropdown: true },
                    image: { uploadCallback: this.imageUploadCallBack }
                  }}
                  onContentStateChange={this.onEditorChange}
                  placeholder="输入想要检测的代码"
                  spellCheck
                  onFocus={() => {
                    console.log('focus')
                  }}
                  onBlur={() => {
                    console.log('blur')
                  }}
                  onTab={() => {
                    console.log('tab')
                    return true
                  }}
                  localization={{ locale: 'zh', translations: { 'generic.add': 'Add' } }}
                  mention={{
                    separator: ' ',
                    trigger: '@',
                    caseSensitive: true,
                    suggestions: [
                      { text: 'A', value: 'AB', url: 'href-a' },
                      { text: 'AB', value: 'ABC', url: 'href-ab' },
                      { text: 'ABC', value: 'ABCD', url: 'href-abc' },
                      { text: 'ABCD', value: 'ABCDDDD', url: 'href-abcd' },
                      { text: 'ABCDE', value: 'ABCDE', url: 'href-abcde' },
                      { text: 'ABCDEF', value: 'ABCDEF', url: 'href-abcdef' },
                      { text: 'ABCDEFG', value: 'ABCDEFG', url: 'href-abcdefg' }
                    ]
                  }}
                />
              </Card>
            </div>
          </Col>
        </Row>
      </div>
    )
  }
}
