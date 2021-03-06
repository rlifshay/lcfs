from .layers.base import BaseLayer, BackingLayerType

class LayerStack:
    '''
    A stack of one or more `LayerGroup`s that a lcfs filesystem maps to.

    Normally a lcfs filesystem will have multiple layer groups in which each
    group corresponds to a specific capacity/latency level. Each group can have
    multiple caching layers to implement multiple caching strategies at each
    capacity/latency level.

    Blocks will be sent to every group in a stack, and read from the first
    group that has the requested block.
    '''

    def __init__(self):
        self._groups = []

    def add(self, group):
        '''Add a new group to the stack.'''
        assert isinstance(group, LayerGroup)
        assert group not in self._groups
        self._groups.append(group)
        return self

    def valid(self):
        '''
        Check if this stack is valid.

        A stack is only valid if it contains at least one group, and if the
        bottom caching layer in the entire stack has at least one layer that is
        a `BackingLayerType`.
        '''
        return len(self._groups) and self._groups[-1].isBacking()

class LayerGroup:
    '''
    A group of one or more caching layers.

    Block writes are sent to the last layer in a group that will accept it
    based on each layer's policies. Block reads are sent to the first layer in
    a group that has the requested block. Reads and writes may not match any
    layer in a group, in which case they will be handled by one or more other
    groups in a properly configured stack.
    '''

    def __init__(self):
        self._layers = []

    def add(self, layer):
        '''Add a new layer to the group.'''
        assert isinstance(layer, BaseLayer)
        assert layer not in self._layers
        self._layers.append(layer)
        return self

    def isBacking(self):
        '''
        Check if this group has a `BackingLayerType` layer as one of the layers.
        '''
        return any(isinstance(layer, BackingLayerType) for layer in self._layers)