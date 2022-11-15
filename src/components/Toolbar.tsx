/**
 * Renders the component.
 *
 * @returns React element
 */
import {
  spacer,
  toolbarButtonClass,
  toolbarClass,
  toolbarNavClass
} from '../style/Toolbar';
import { ActionButton } from './ActionButton';
import { reloadIcon } from '../style/icon';
import { requestAPI } from '../handler';
import React from 'react';
// import { CodeFrame } from './CodeFrame';

export const Toolbar: React.FunctionComponent = () => {
  const [text, setText] = React.useState('There has been no snapshot taken.');

  const handleClick = async (): Promise<void> => {
    const snapshot = await requestAPI<any>('code');
    setText(snapshot.code);
  };

  return (
    <nav className={toolbarClass}>
      <div className={toolbarNavClass}>
        <ActionButton
          className={toolbarButtonClass}
          icon={reloadIcon}
          title="Take snapshot"
          onClick={handleClick}
        />
      </div>
      <div className={spacer} />
      <div>{text}</div>
    </nav>
  );
};
// type ToolbarState = {
//   text: string;
// };
//
// export class Toolbar extends React.Component {
//   state: ToolbarState = {
//     text: 'There has been no snapshot taken.'
//   };
//   render(): React.ReactElement {
//     const { text } = this.state;
//     return (
//       <div className={toolbarClass}>
//         {this._renderSuggestionReq()}
//         {/*{this._renderSuggestion()}*/}
//         {/*{this._renderCodeWindow()}*/}
//         <div>{text}</div>
//       </div>
//     );
//   }
//
//   // private suggestion = 'There has been no snapshot taken.';
//
//   /**
//    * Renders the top navigation.
//    *
//    * @returns React element
//    */
//   private _renderSuggestionReq(): React.ReactElement {
//     return (
//       <div className={toolbarNavClass}>
//         <span className={spacer} />
//         <ActionButton
//           className={toolbarButtonClass}
//           icon={reloadIcon}
//           onClick={this._onRefresh}
//           title={'snapshot'}
//         />
//       </div>
//     );
//   }
//
//   /**
//    * Callback invoked upon clicking a button to pull the latest changes.
//    *
//    * @param event - event object
//    * @returns a promise which resolves upon pulling the latest changes
//    */
//   private _onRefresh = async (): Promise<void> => {
//     // GET request -> BE to FE
//     let data;
//     let arr: string[];
//     try {
//       data = await requestAPI<any>('code');
//       arr = Object.values(data);
//       console.log(arr);
//       this.setState({ ...data });
//       console.log(this.state.text);
//     } catch (reason) {
//       console.error(`Error on GET /simic/data.\n${reason}`);
//     }
//   };
//
//   // private _renderSuggestion(): React.ReactElement {
//   //   return <CodeFrame></CodeFrame>;
//   // }
// }
