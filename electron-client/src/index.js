const { app, BrowserWindow } = require('electron');
const path = require('path');
const load_window = require('./static/js/create_data');
const load_window2 = require('./static/js/use_data');

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  try {
    load_window();
  } catch (error) {
    console.log('Error:', error);
  }

  try {
    load_window2();
  } catch (error) {
    console.log('Error:', error);
  }

  // Open the DevTools.
  // mainWindow.webContents.openDevTools();
};


app.on('ready', createWindow);

// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

