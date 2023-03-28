from uplink import Consumer, get, post, Body, Query


class Client:
    def get(self, *args, **kwargs):
        raise NotImplemented


class Okra(Consumer):
    @post("/products/kyc/bvn-verify")
    def verify_bvn(self, bvn_request: Body):
        pass

    @post('/products/kyc/nuban-verify')
    def verify_account(self, nuban_request: Body):
        pass


class Appzone(Consumer):
    @get("/whatever/get-bvn")
    def verify_bvn(self, bvn: Query):
        pass


class Nibss(Consumer):
    @get("/verify/the/damn/bvn")
    def verify_bvn(self, bvn: Query):
        pass
