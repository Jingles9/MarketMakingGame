BUY = 'buy'
SELL = 'sell'

from flask_table import Table, Col
class ItemTable(Table):
    bid_depth = Col('Bid Depth')
    bid = Col('Bid')
    ask = Col('Ask')
    ask_depth = Col('Ask Depth')

class Item():
    def __init__(self, bid_depth, bid, ask, ask_depth):
        self.bid_depth = bid_depth
        self.bid = bid
        self.ask = ask
        self.ask_depth = ask_depth

class Exchange():
    
    def __init__(self):
        self.bids = dict()
        self.asks = dict()
            
    def process_aggressive(self, aggressor, side):
        if side == BUY and len(self.asks) > 0:
            ask = min(self.asks.keys())
            aggressor.execute_trade(BUY, ask)
            seller = self.asks[ask][0]
            seller.fill_order(SELL)
            self.asks[ask].remove(seller)
            if len(self.asks[ask]) == 0:
                del self.asks[ask]
        if side == SELL and len(self.bids) > 0:
            bid = max(self.bids.keys())
            aggressor.execute_trade(SELL, bid)
            buyer = self.bids[bid][0]
            buyer.fill_order(BUY)
            self.bids[bid].remove(buyer)
            if len(self.bids[bid]) == 0:
                del self.bids[bid]
        
    def process_passive(self, participant, bid=None, ask=None):
        if (bid is not None and ask is not None) and (bid >= ask):
            return
        if bid is not None:
            if len(self.asks) == 0 or bid < min(self.asks.keys()):
                empty_val = None
                for (value, participants) in self.bids.items():
                    if participant in participants:
                        participants.remove(participant)
                        if len(participants) == 0:
                            empty_val = value
                if empty_val is not None:
                    del self.bids[empty_val]
                if (bid in self.bids.keys()):
                    self.bids[bid].append(participant)
                else:
                    self.bids[bid] = [participant]
                participant.place_order(BUY, bid)
        if ask is not None:
            if len(self.bids) == 0 or ask > max(self.bids.keys()):
                empty_val = None
                for (value, participants) in self.asks.items():
                    if participant in participants:
                        participants.remove(participant)
                        if len(participants) == 0:
                            empty_val = value
                if empty_val is not None:
                    del self.asks[empty_val]
                if (ask in self.asks.keys()):
                    self.asks[ask].append(participant)
                else:
                    self.asks[ask] = [participant]
                participant.place_order(SELL, ask)
    
    def print_book(self):
        print('Bids')
        for (bid, participants) in self.bids.items():
            print(str(len(participants)) + '@' + str(bid))
        print('Asks')
        for (ask, participants) in self.asks.items():
            print(str(len(participants)) + '@' + str(ask))

    def get_table(self):
        items = []
        if len(self.bids) == 0:
            bids = []
        else:
            keys = list(self.bids.keys())
            keys.sort()
            bids = [dict({'bid': str(key), 'qty': str(len(self.bids[key]))}) for key in keys]
        if len(self.asks) == 0:
            asks = []
        else:
            keys = list(self.asks.keys())
            keys.sort()
            asks = [dict({'ask': str(key), 'qty': str(len(self.asks[key]))}) for key in keys]
        for i in range(max(len(self.bids), len(self.asks))):
            if i > len(self.bids) - 1:
                bid_depth = ""
                bid = ""
            else:
                bid_depth = bids[i]['qty']
                bid = bids[i]['bid']
            if i > len(self.asks) - 1:
                ask_depth = ""
                ask = ""
            else:
                ask_depth = asks[i]['qty']
                ask = asks[i]['ask']
            items.append(Item(bid_depth, bid, ask, ask_depth))
        return ItemTable(items)
