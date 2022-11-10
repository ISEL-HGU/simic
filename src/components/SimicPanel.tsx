/**
 * React component for rendering a panel for performing Simic operations.
 */
import React from 'react';
import { Toolbar } from './Toolbar';
import { panelWrapperClass } from '../style/SimicPanel';

export class SimicPanel extends React.Component {
  /**
   * Renders the component.
   *
   * @returns React element
   */
  render(): React.ReactElement {
    return (
      <div className={panelWrapperClass}>
        <React.Fragment>{this._renderToolbar()}</React.Fragment>
      </div>
    );
  }
  /**
   * Renders a toolbar.
   *
   * @returns React element
   */
  private _renderToolbar(): React.ReactElement {
    return <Toolbar />;
  }
}
