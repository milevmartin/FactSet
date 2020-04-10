#script deletes the last written file located at C:\datacache
#script has to be executed on each node on the cluster - this can be performed using GPO or another configuration management tool - like puppet
# Create Log folder where the log files are stored
# this tep is optional we can use any other folder

$LogDirCheck = Test-Path C:\logs

if ($LogDirCheck -eq $false){
mkdir C:\logs\
}

#get free disk space using WMI 
$computer = gc env:computername #we need to specify a target for the WMI query
$disk = Get-WmiObject Win32_LogicalDisk -ComputerName $computer -Filter "DeviceID='C:'" | Select-Object Size,FreeSpace #quering the Win32_LogicalDisk NS
$FreeSpacePRCNT = ($disk.FreeSpace / $disk.Size)*100 #converting the values to be human readable

    
#execute the bellow script untill the free space is more than 20%
while ($FreeSpacePRCNT -lt 20) {

#Get the oldest log files and Remove the file oldest log file        
    try {


			$file = Get-ChildItem C:\datacache | Sort-Object -Property LastWriteTime | select -first 1 #get the oldes file
			$date = Get-Date # get the date
				if ($file){
							Get-ChildItem C:\datacache | Sort-Object -Property LastWriteTime | select -first 1 | Remove-Item # remove the oldes file
							"$date $file.name is deleted" | Out-File -FilePath C:\logs\removedfiles.log -Append #write the results to the log
				} else{
						exit;
				}		       
        }

    catch [System.IO.FileNotFoundException],[System.IO.IOException]{
 
        "$date $file.name was not fould check the error $_.ScriptStackTrace " | Out-File -FilePath C:\logs\removedfiles.log -Append
	
	exit;     
        }
    catch {
        
        "$date unable to delete the file $file Unknown error: $_.ScriptStackTrace " | Out-File -FilePath C:\logs\removedfiles.log -Append #write an error message to the log
        
	exit;        
        }                       
}


 
    

