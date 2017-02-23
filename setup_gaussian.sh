# GAUSSIAN 09
export g09root=/Applications/gaussian
export GAUSS_SCRDIR=/scratch
export PATH=$g09root/g09/bin:$PATH
GAUSSIANENVFILE=/user/zw/Applications/Gaussian/g09.profile
if [[ -f $g09root/g09/bin/g09 ]]; then
    source /user/zw/Applications/Gaussian/g09.profile
fi

# TINKER
export TINKER=/user/ponder/tinker
export PATH=$TINKER/bin:$PATH
alias a09="less $TINKER/params/amoeba09.prm"

export TINKER_MT=/user/ponder/tinker-iso
export PATH=$TINKER_MT/bin:$PATH
alias a13='less $TINKER/params/amoebapro13.prm'