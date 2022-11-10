import { ReactWidget } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import React from 'react';
import { simicWidgetStyle } from '../style/SimicWidgetStyle';
import { StylesProvider } from '@material-ui/core/styles';
import { SimicPanel } from '../components/SimicPanel';
/**
 * A class that exposes the simic plugin Widget.
 */
export class SimicWidget extends ReactWidget {
  constructor(options?: Widget.IOptions) {
    super(options);
    this.node.id = 'simic-widget';
    this.addClass(simicWidgetStyle);
  }

  /**
   * Render the content of this widget using the virtual DOM.
   *
   * This method will be called anytime the widget needs to be rendered, which
   * includes layout triggered rendering.
   */
  render(): JSX.Element {
    console.log("why aren't you rendering?");
    return (
      <StylesProvider injectFirst>
        <React.Fragment>
          <SimicPanel></SimicPanel>
        </React.Fragment>
      </StylesProvider>
    );
  }
}
