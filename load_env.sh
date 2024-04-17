if [ ! -f .env.local ]
then
  export $(cat .env.local | xargs)
fi