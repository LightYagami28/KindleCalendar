# Changelog

## Update 03/05/2024

### modified in client.js:

- Updated JavaScript syntax to use arrow functions, let and const instead of var, and template literals for string interpolation.
- Improved event handling by using addEventListener instead of assigning event handlers directly to properties like onclick.
- Enhanced error handling and readability.

### modified in screenshot.py:

- Grouped imported modules together at the top of the script.
- Followed PEP8 naming conventions for variables and function names.
- Improved code comments for better readability and understanding.
- Used f-strings for string formatting.
- Utilized a dictionary for mapping day names to offsets.
- Removed unnecessary imports and commented-out code.
- Updated code formatting to be consistent.

### modified in server.js:

- Changed the import statement for WebSocket from require('ws-plus-hixie') to require('ws').
- Renamed the WsHixie variable to WebSocket for clarity.
- Used let and const instead of var.
- Updated the watcher.on('change') callback function to use let instead of var for the now variable.
- Applied consistent semicolon usage.
- Improved readability by adding comments to clarify code blocks.