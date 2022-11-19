import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, IFrame } from '@jupyterlab/apputils';

import { PageConfig } from '@jupyterlab/coreutils';

// import { ILauncher } from '@jupyterlab/launcher';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { ToolbarButton } from '@jupyterlab/apputils';
import { DocumentRegistry } from '@jupyterlab/docregistry';

import {
  // NotebookActions,
  NotebookPanel,
  INotebookModel
} from '@jupyterlab/notebook';

import { requestAPI } from './handler';
import { SimicWidget } from './widgets/SimicWidget';
import { logoIcon, snapshotIcon } from './style/icon';

/**
 * The command IDs used by the server extension plugin.
 */
namespace CommandIDs {
  export const get = 'server:get-file';
}

/**
 * Initialization data for the server-extension-example extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'plugin:simic',
  autoStart: true,
  optional: [],
  requires: [ICommandPalette],
  activate: async (app: JupyterFrontEnd, palette: ICommandPalette) => {
    console.log('JupyterLab extension server-extension-example is activated!');

    const button = new ButtonExtension();
    const gitPlugin = new SimicWidget();
    gitPlugin.id = 'jp-git-sessions';
    gitPlugin.title.icon = logoIcon;
    gitPlugin.title.caption = 'Simic';

    app.shell.add(gitPlugin, 'left', { rank: 200 });

    app.docRegistry.addWidgetExtension('Notebook', button);

    // POST request -> FE to BE
    const dataToSend = { snapshot: 'code snapshot' };
    try {
      const reply = await requestAPI<any>('code', {
        body: JSON.stringify(dataToSend),
        method: 'POST'
      });
      console.log(reply);
    } catch (reason) {
      console.error(
        `Error on POST /jlab-ext-example/code ${dataToSend}.\n${reason}`
      );
    }

    // GET request -> BE to FE
    // try {
    //   const data = await requestAPI<any>('hello');
    //   console.log(data);
    // } catch (reason) {
    //   console.error(`Error on GET /simic/hello.\n${reason}`);
    // }

    const { commands, shell } = app;
    const command = CommandIDs.get;
    const category = 'Extension Examples';

    commands.addCommand(command, {
      label: 'Get Server Content in a IFrame Widget',
      caption: 'Get Server Content in a IFrame Widget',
      execute: () => {
        const widget = new IFrameWidget();
        shell.add(widget, 'main');
      }
    });

    palette.addItem({ command, category: category });

    // if (launcher) {
    //   // Add launcher
    //   launcher.add({
    //     command: command,
    //     category: category,
    //   });
    // }
  }
};

export default extension;

class IFrameWidget extends IFrame {
  constructor() {
    super();
    const baseUrl = PageConfig.getBaseUrl();
    this.url = baseUrl + 'jlab-ext-example/public/index.html';
    this.id = 'doc-example';
    this.title.label = 'Server Doc';
    this.title.closable = true;
    this.node.style.overflowY = 'auto';
  }
}

/**
 * A notebook widget extension that adds a button to the toolbar.
 */
export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  /**
   * Create a new extension for the notebook panel widget.
   *
   * @param panel Notebook panel
   * @param context Notebook context
   * @returns Disposable on the added button
   */
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    const takeSnapshot = async () => {
      if (this._fileCount === 2) {
        this._fileCount = 1;
      }
      this._fileCount += 1;
      this._snapCount ++;
      const dataToSend = {
        snapshot:
          panel.content.widgets[panel.content.activeCellIndex].model.value
            .text +
          '!@#$%' +
          this._fileCount +
          '!@#$%' +
          this._snapCount
      };
      try {
        const reply = await requestAPI<any>('code', {
          body: JSON.stringify(dataToSend),
          method: 'POST'
        });
        console.log(reply);
      } catch (reason) {
        console.error(
          `Error on POST /jlab-ext-example/code ${dataToSend}.\n${reason}`
        );
      }
    };
    const button = new ToolbarButton({
      className: 'snapshot-button',
      icon: snapshotIcon,
      onClick: takeSnapshot,
      tooltip: 'take snapshot of the current state of your source code.'
    });

    panel.toolbar.insertItem(10, 'clearOutputs', button);
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
  private _snapCount = 0;
  private _fileCount = 0;
}
