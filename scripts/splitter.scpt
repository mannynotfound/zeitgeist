#!/usr/bin/osascript
(* 
  This script launches multiple iTerm panes with the `twitter_search.py` utility.
  Pass the terms you would like to search as a `term_names` environment variable 
  comma seperated string delimited

  eg `term_names="google,apple,uber"`
*)

on theSplit(theString, theDelimiter)
  set oldDelimiters to AppleScript's text item delimiters
  set AppleScript's text item delimiters to theDelimiter
  set theArray to every text item of theString
  set AppleScript's text item delimiters to oldDelimiters
  return theArray
end theSplit

set termNames to system attribute "term_names"
set terms to my theSplit(termNames, ",")
set num_terms to count of terms

tell application "iTerm"
  create window with default profile
  tell application "System Events" to key code 36 using command down
  delay 1
  repeat with n from 1 to num_terms
    tell current session of current window
      write text "python3 ~/Sites/zeitgeist/twitter_search.py -t \"" & (item n of terms) & "\""
      if n is not equal to num_terms
        tell application "System Events" to keystroke "D" using command down
      end if
      delay 0.2
    end tell
  end repeat
end tell
