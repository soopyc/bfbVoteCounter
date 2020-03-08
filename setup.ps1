Write-Host "Welcome to this short configuration and setup script."

Write-Host "We will be installing a few files in your system, and this should be automated, unless something horrible happened."
Write-Host "In that case, tell me in https://github.com/kcomain/bfbVoteCounter/issues/new"

Write-Host "Checking if the old archive is still present..."
$tp = test-path temp932183629.zip
if ($tp -eq $true) {
	Write-Host "Temporary file found, deleting..."
	Remove-Item ./temp932183629.zip
}

$tp = test-path bfbVoteCounter
if ($tp -eq $true) {
	Write-Host "Temporary file found, deleting..."
	Remove-Item ./temp932183629.zip
}

Write-Host "Downloading archive..."
Invoke-WebRequest https://github.com/kcomain/bfbVoteCounter/archive/master.zip -o temp932183629.zip

Write-Host "Unzipping files..."
Expand-Archive ./temp932183629.zip -DestinationPath ./

Write-Host "Deleting temp archive..."
Remove-Item ./temp932183629.zip

Write-Host "Changing directory name..."
$dirname = Read-Host "What do you want the new folder name be(renamed from bfbVoteCounter-master)? ['bfbVoteCounter']"
if ($dirname -eq ""){
$dirname= "bfbVoteCounter"
}

Move-Item ./bfbVoteCounter-master $dirname