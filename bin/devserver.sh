#!/bin/bash

BASE_DIR=`dirname $0`
WORKING_DIR=`pwd`

echo ""
echo "This script starts all the services needed to develop the"
echo "api locally."
echo "-------------------------------------------------------------------"

# Clear out any compiled alembic revisions. This is necessary to avoid the case
# in which an alembic revision from a different branch exists as a compiled revision
# since they are not part of the repo.
echo "Removing all compiled alembic revisions..."
ALEMBIC_PATH="/alembic/versions/*.pyc"
rm -r $WORKING_DIR$ALEMBIC_PATH
echo "-------------------------------------------------------------------"

# Default parameters
#
HOST="127.0.0.1"
PORT="5000"
PROCFILE_PATH="/bin/procfiles/Procfile.dev"
PROCFILE=$WORKING_DIR$PROCFILE_PATH

# Parse the command line flags.
#
while getopts ":np:f:" opt; do
  case $opt in
    n)
      # Get the IP address on a mac.  Only works on a mac.
      #
      HOST=`ifconfig | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}'|head -n1`
      ;;

    p)
      # Set the port
      #
      PORT=${OPTARG}
      ;;

    f)
      # Set the Procfile
      #
      PROCFILE=${OPTARG}
      if [[ ! -e "$PROCFILE" ]]; then
        die "...your specified $PROCFILE does not exist"
      fi
      ;;

    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

# Custom die function.
#
die() { echo >&2 -e "\nRUN ERROR: $@\n"; exit 1; }

# Check for required programs: coffee, redis-server, and Postgres.app
#
COFFEE=$(command -v coffee || die "...Error: coffee is not in your path!")
REDIS=$(command -v redis-server || die "...Error: redis-server is not in your path!")
HONCHO=$(command -v honcho || command -v foreman || die "...Error: honcho/foreman is not in your path!  Are you in the right virtualenv?")
POSTGRES="/Applications/Postgres.app"
if [ ! -d "$POSTGRES" ]; then
    die "...Error: cannot find Postgres.app"
fi

# Check for .env file
#
if [[ ! -e "$BASE_DIR/../.env" ]]; then
    die "...You need to have a .env file at $BASE_DIR/../.env"
fi

# Add node modules to path for webassets
#
if [[ -d "$BASE_DIR/../node_modules" ]]; then
  READLINK=$(command -v greadlink || command -v readlink || die "...Error: readlink is not in your path!  Are you in the right virtualenv?")
  NODE_BIN=$($READLINK -f $BASE_DIR/../node_modules/.bin)
  export PATH=$NODE_BIN:$PATH
fi


# Print config
#
echo ""
echo "Configuration:"
echo -e "\tPROCFILE: $PROCFILE"
echo -e "\tCOFFEE: $COFFEE"
echo -e "\tREDIS: $REDIS"
echo -e "\tHONCHO: $HONCHO"
echo -e "\tPOSTGRES: $POSTGRES"
echo -e "\tHOST: $HOST"
echo -e "\tPORT: $PORT"
echo -e "\tPATH: $PATH"
echo ""
echo "-------------------------------------------------------------------"

# Start Postgres, which daemonizes, so cannot be used
# with foreman/honcho
#
open $POSTGRES

# Start the other processes.  See bin/Procfile.dev
#
HOST=$HOST PORT=$PORT $HONCHO start -f $PROCFILE

