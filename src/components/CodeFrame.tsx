import React, { Component } from 'react';

export class CodeFrame extends Component<CodeFrameProps, CodeFrameState> {
  state: CodeFrameState = {
    text: 'There has been no snapshot taken.'
  };

  render() {
    // const { text } = this.state;
    // const { code } = this.props;
    return <div></div>;
  }
}
export type CodeFrameProps = { code?: string };
export type CodeFrameState = { text: string };
