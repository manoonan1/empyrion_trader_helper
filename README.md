# **Requirements to get started**

Ensure you have Python 3.10 or greater installed as the switch case capabilities were added in that version.

Ensure pip is on your system or python virtual environment (it is often packaged with python installs so it should be there)

Run:
`pip install -r requirements.txt`
To ensure the libraries used in this script are installed.


# **Running the script**
In the directory you pulled the repo from, run:
```
python3 TradeHelper.py
```

A number of options will appear that look like this:
```
Please input the following option for your needs:
(1): Looking to sell
(2): Looking to buy
(3): Looking for best place to sell
(4): Looking for best place to buy
(5): Looking for trade route

option?
```
When prompted, choose your option, then you will be asked to name the item you want to learn about, the example choose option 5.
```
option? 5

What item are you looking to find a trade route for? Leather
```
You will recieve an output that will look something like this:
```
              buy_from buy_rate in_stock         sell_to sell_rate will_buy
0  Talon LeatherFarmer      0.8   25-125  Bertram's Arms       2.5    20-80
```
