const initialState = [
    {
        name: 'table',
        uuid: 'f16ca3d0-fe83-4b1e-8eea-7e35db3f6b0f',
        type: 'FeatureTable[Frequency]'
    },
    {
        name: 'phylogeny',
        uuid: '908dece5-db23-4562-ad03-876bb5750145',
        type: 'Phylogeny'
    }
];

const artifacts = (state = initialState, action) => {
    switch (action.type) {
    case 'DELETE_ARTIFACT': {
        // TODO, make it actually do something
        const newState = state.filter((_, index) => index !== action.index);
        return newState;
    }
    default:
        break;
    }
    return state;
};

export default artifacts;
