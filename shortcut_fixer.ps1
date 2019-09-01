$oldPrefix = "<current_path_here>"
$newPrefix = "<new_path_here>"

$searchPath = "<where_are_we_running>"

$dryRun = $TRUE

$shell = new-object -com wscript.shell

if ( $dryRun ) {
   write-host "Executing dry run" -foregroundcolor green -backgroundcolor black
} else {
   write-host "Executing real run" -foregroundcolor red -backgroundcolor black
}

dir $searchPath -filter *.lnk -recurse | foreach {
   $lnk = $shell.createShortcut( $_.fullname )
   $oldPath= $lnk.targetPath

   $lnkRegex = "^" + [regex]::escape( $oldPrefix ) 

   if ( $oldPath -match $lnkRegex ) {
      $newPath = $oldPath -replace $lnkRegex, $newPrefix

      write-host "Found: " + $_.fullname -foregroundcolor yellow -backgroundcolor black
      write-host " Replace: " + $oldPath
      write-host " With:    " + $newPath

      if ( !$dryRun ) {
         $lnk.targetPath = $newPath
         $lnk.Save()
      }
   }
}