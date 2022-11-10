/**
 * Renders the component.
 *
 * @returns React element
 */
import React from 'react';
import {
  spacer,
  toolbarButtonClass,
  toolbarClass,
  toolbarNavClass
} from '../style/Toolbar';
import { ActionButton } from './ActionButton';
import { reloadIcon } from '../style/icon';
import { requestAPI } from '../handler';

export class Toolbar extends React.Component {
  render(): React.ReactElement {
    return (
      <div className={toolbarClass}>
        {this._renderSuggestionReq()}
        {/*{this._renderClearSnapshots()}*/}
        {/*{this._renderCodeWindow()}*/}
      </div>
    );
  }

  /**
   * Renders the top navigation.
   *
   * @returns React element
   */
  private _renderSuggestionReq(): React.ReactElement {
    return (
      <div className={toolbarNavClass}>
        <span className={spacer} />
        <ActionButton
          className={toolbarButtonClass}
          icon={reloadIcon}
          onClick={this._onSnapshot}
          title={'snapshot'}
        />
      </div>
    );
  }

  /**
   * Callback invoked upon clicking a button to pull the latest changes.
   *
   * @param event - event object
   * @returns a promise which resolves upon pulling the latest changes
   */
  private _onSnapshot = async (): Promise<void> => {
    const dataToSend = { snapshot: 'code snapshot' };
    try {
      const reply = await requestAPI<any>('code', {
        body: JSON.stringify(dataToSend),
        method: 'POST'
      });
      console.log(reply);
    } catch (reason) {
      console.error(`Error on POST /simic/hello ${dataToSend}.\n${reason}`);
    }
  };
}
