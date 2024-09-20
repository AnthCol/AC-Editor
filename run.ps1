param(
    [switch]$test,
    [switch]$install
)

if ($test) {
    pytest
}
elseif ($install) {
    python3 -m pip install -r requirements.txt
}
else {
    python3 -m src.ac_editor
}

