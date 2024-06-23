$acl = Get-Acl HKLM:\Software\Policies

$person = [System.Security.Principal.NTAccount]"Users"
$access = [System.Security.AccessControl.RegistryRights]"FullControl"
$propagation = [System.Security.AccessControl.PropagationFlags]"None"
$type = [System.Security.AccessControl.AccessControlType]"Allow"

$rule = New-Object System.Security.AccessControl.RegistryAccessRule ("$person","$access",@("ObjectInherit","ContainerInherit"),"$propagation","$type")
$acl.SetAccessRule($rule)
$acl |Set-Acl -Path HKLM:\Software\Policies
